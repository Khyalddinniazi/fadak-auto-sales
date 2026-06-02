import os
import secrets
import sqlite3
from datetime import date, datetime
from functools import wraps

from flask import (
    Flask,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from seed_data import SERVICE_SEED, vehicles_with_images

# Base directory for predictable relative paths.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "mechanic_shop.db")

# Treat anything other than an explicit "1"/"true" as production.
DEBUG = os.environ.get("FLASK_DEBUG", "0").lower() in {"1", "true", "yes"}

app = Flask(__name__)
# In production a real SECRET_KEY must be supplied via the environment.
# We only fall back to a random per-process key in debug so sessions still work locally.
_secret = os.environ.get("SECRET_KEY")
if not _secret:
    if not DEBUG:
        raise RuntimeError(
            "SECRET_KEY environment variable is required when FLASK_DEBUG is off. "
            "Set it before starting the app in production."
        )
    _secret = secrets.token_hex(32)
app.config["SECRET_KEY"] = _secret

# Harden the session cookie for production.
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=not DEBUG,
)

# Admin credentials come from the environment in production; sensible demo
# defaults keep local development friction-free. The password is never stored
# in plain text at rest — we hash it once at startup and compare hashes.
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
_admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
ADMIN_PASSWORD_HASH = generate_password_hash(_admin_password)

# Fadak Auto Sales — business contact (shown site-wide).
SITE = {
    "name": "Fadak Auto Sales",
    "tagline": "Premium vehicles & trusted auto service in Tacoma, WA",
    "address": "5110 131st Street Ct E, Tacoma, WA 98446",
    "phone": "(253) 777-5796",
    "email": "Autosalesfadak@gmail.com",
    "hours": "Mon–Sat: 9:00 AM – 6:00 PM | Sun: By appointment",
}


@app.context_processor
def inject_site():
    """Make dealership info available in every template."""
    return {"site": SITE, "debug": DEBUG}


# ---------- CSRF protection ----------
def generate_csrf_token():
    """Return (and cache) a per-session CSRF token."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


@app.context_processor
def inject_csrf_token():
    """Expose csrf_token() to every template."""
    return {"csrf_token": generate_csrf_token}


@app.before_request
def csrf_protect():
    """Reject state-changing requests that lack a valid CSRF token."""
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        sent_token = request.form.get("csrf_token") or request.headers.get("X-CSRFToken")
        expected = session.get("csrf_token")
        if not expected or not sent_token or not secrets.compare_digest(sent_token, expected):
            abort(400)


@app.after_request
def set_security_headers(response):
    """Add baseline security headers to every response."""
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    return response


# ---------- Database helpers ----------
def get_db():
    """Return a database connection tied to this request context."""
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    """Close database connection after each request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create database tables and seed starter records."""
    os.makedirs(DB_DIR, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    cursor.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            vehicle_make TEXT NOT NULL,
            vehicle_model TEXT NOT NULL,
            vehicle_year INTEGER,
            service_type TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            mileage INTEGER NOT NULL,
            price REAL NOT NULL,
            condition TEXT NOT NULL,
            vin TEXT,
            description TEXT,
            image_url TEXT,
            status TEXT NOT NULL DEFAULT 'Available'
        );

        CREATE TABLE IF NOT EXISTS services (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL,
            estimated_price REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS inquiries (
            inquiry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );
        """
    )

    # Add any missing services (safe to run every startup).
    for service_name, description, estimated_price in SERVICE_SEED:
        cursor.execute(
            """
            INSERT OR IGNORE INTO services (service_name, description, estimated_price)
            VALUES (?, ?, ?)
            """,
            (service_name, description, estimated_price),
        )

    # Remove legacy demo VINs so we do not duplicate Toyota/Honda rows after expanding inventory.
    legacy_vins = (
        "VIN-TOY-CAMRY%",
        "VIN-HON-ACCORD%",
        "VIN-FOR-F150%",
        "VIN-BMW-3SERIES%",
        "VIN-TES-MODEL3%",
        "VIN-NIS-ALTIMA%",
        "VIN-CHE-SILV%",
        "VIN-HYU-SONATA%",
    )
    for pattern in legacy_vins:
        cursor.execute("DELETE FROM vehicles WHERE vin LIKE ?", (pattern,))

    # Add vehicles by unique VIN until we have the full demo lot (22 cars).
    for vehicle in vehicles_with_images():
        vin = vehicle[6]
        exists = cursor.execute(
            "SELECT vehicle_id FROM vehicles WHERE vin = ?", (vin,)
        ).fetchone()
        if exists:
            continue
        cursor.execute(
            """
            INSERT INTO vehicles
            (year, make, model, mileage, price, condition, vin, description, image_url, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            vehicle,
        )

    # Refresh broken or placeholder image URLs on existing rows.
    # We overwrite empty/placeholder values and any stock Unsplash URL (some of
    # the original photo IDs went dead and now 404). Custom images set by an
    # admin from a different host are left untouched.
    for vehicle in vehicles_with_images():
        vin, image_url = vehicle[6], vehicle[8]
        cursor.execute(
            """
            UPDATE vehicles
            SET image_url = ?
            WHERE vin = ?
              AND image_url IS NOT ?
              AND (
                    image_url IS NULL
                    OR TRIM(image_url) = ''
                    OR LOWER(image_url) LIKE '%placeholder%'
                    OR image_url LIKE 'https://images.unsplash.com/%'
              )
            """,
            (image_url, vin, image_url),
        )

    db.commit()
    db.close()


# ---------- Auth / validation helpers ----------
def admin_required(view):
    """Protect admin routes so only logged-in admin can access them."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please log in to access the admin dashboard.", "warning")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)

    return wrapped


def parse_int(value, default=None):
    """Safely parse integer form values."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_float(value, default=None):
    """Safely parse float form values."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def validate_appointment(form_data):
    """Validate appointment request fields from customer form."""
    required_fields = [
        ("full_name", "Full name is required."),
        ("email", "Email is required."),
        ("phone", "Phone number is required."),
        ("vehicle_make", "Vehicle make is required."),
        ("vehicle_model", "Vehicle model is required."),
        ("service_type", "Service type is required."),
        ("preferred_date", "Preferred date is required."),
        ("preferred_time", "Preferred time is required."),
    ]

    errors = []
    for field_name, message in required_fields:
        if not form_data.get(field_name, "").strip():
            errors.append(message)

    if form_data.get("email") and "@" not in form_data.get("email", ""):
        errors.append("Please enter a valid email address.")

    year = form_data.get("vehicle_year", "").strip()
    if year and (not year.isdigit() or len(year) != 4):
        errors.append("Vehicle year must be a valid 4-digit year.")

    preferred_date = form_data.get("preferred_date", "").strip()
    if preferred_date:
        try:
            requested = datetime.strptime(preferred_date, "%Y-%m-%d").date()
            if requested < date.today():
                errors.append("Preferred date cannot be in the past.")
        except ValueError:
            errors.append("Preferred date is invalid.")

    return errors


# ---------- Public routes ----------
@app.route("/")
def index():
    db = get_db()
    featured_vehicles = db.execute(
        "SELECT * FROM vehicles ORDER BY vehicle_id DESC LIMIT 8"
    ).fetchall()
    services = db.execute(
        "SELECT * FROM services ORDER BY service_name ASC LIMIT 10"
    ).fetchall()
    return render_template(
        "index.html", featured_vehicles=featured_vehicles, services=services
    )


@app.route("/inventory")
def inventory():
    db = get_db()

    search = request.args.get("search", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    year = request.args.get("year", "").strip()
    condition = request.args.get("condition", "").strip()

    query = "SELECT * FROM vehicles WHERE 1=1"
    params = []

    if search:
        query += " AND (make LIKE ? OR model LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if min_price:
        query += " AND price >= ?"
        params.append(parse_float(min_price, 0))
    if max_price:
        query += " AND price <= ?"
        params.append(parse_float(max_price, 9999999))
    if year:
        query += " AND year = ?"
        params.append(parse_int(year, 0))
    if condition:
        query += " AND condition = ?"
        params.append(condition)

    query += " ORDER BY year DESC, make ASC"

    vehicles = db.execute(query, params).fetchall()
    available_years = db.execute("SELECT DISTINCT year FROM vehicles ORDER BY year DESC").fetchall()
    conditions = db.execute("SELECT DISTINCT condition FROM vehicles ORDER BY condition ASC").fetchall()

    return render_template(
        "inventory.html",
        vehicles=vehicles,
        available_years=available_years,
        conditions=conditions,
        filters={
            "search": search,
            "min_price": min_price,
            "max_price": max_price,
            "year": year,
            "condition": condition,
        },
    )


@app.route("/vehicles/<int:vehicle_id>")
def vehicle_detail(vehicle_id):
    db = get_db()
    vehicle = db.execute("SELECT * FROM vehicles WHERE vehicle_id = ?", (vehicle_id,)).fetchone()
    if vehicle is None:
        flash("Vehicle not found.", "danger")
        return redirect(url_for("inventory"))
    return render_template("vehicle_detail.html", vehicle=vehicle)


@app.route("/services")
def services():
    db = get_db()
    all_services = db.execute("SELECT * FROM services ORDER BY service_name ASC").fetchall()
    return render_template("services.html", services=all_services)


@app.route("/appointment", methods=["GET", "POST"])
def appointment():
    db = get_db()
    service_names = db.execute("SELECT service_name FROM services ORDER BY service_name ASC").fetchall()

    if request.method == "POST":
        errors = validate_appointment(request.form)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "appointment.html",
                service_names=service_names,
                min_date=date.today().isoformat(),
            )

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        vehicle_make = request.form.get("vehicle_make", "").strip()
        vehicle_model = request.form.get("vehicle_model", "").strip()
        vehicle_year = parse_int(request.form.get("vehicle_year", "").strip(), None)
        service_type = request.form.get("service_type", "").strip()
        preferred_date = request.form.get("preferred_date", "").strip()
        preferred_time = request.form.get("preferred_time", "").strip()
        notes = request.form.get("notes", "").strip()

        # Reuse existing customer by email/phone where possible.
        customer = db.execute(
            "SELECT customer_id FROM customers WHERE email = ? AND phone = ?",
            (email, phone),
        ).fetchone()

        if customer:
            customer_id = customer["customer_id"]
            db.execute(
                "UPDATE customers SET name = ? WHERE customer_id = ?",
                (full_name, customer_id),
            )
        else:
            cursor = db.execute(
                "INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)",
                (full_name, email, phone),
            )
            customer_id = cursor.lastrowid

        db.execute(
            """
            INSERT INTO appointments
            (customer_id, vehicle_make, vehicle_model, vehicle_year, service_type,
             appointment_date, appointment_time, notes, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
            """,
            (
                customer_id,
                vehicle_make,
                vehicle_model,
                vehicle_year,
                service_type,
                preferred_date,
                preferred_time,
                notes,
                datetime.utcnow().isoformat(),
            ),
        )
        db.commit()

        flash("Your appointment has been submitted successfully.", "success")
        return redirect(url_for("appointment"))

    return render_template(
        "appointment.html",
        service_names=service_names,
        min_date=date.today().isoformat(),
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all required contact fields.", "danger")
        elif "@" not in email:
            flash("Please enter a valid email address.", "danger")
        else:
            db = get_db()
            db.execute(
                """
                INSERT INTO inquiries (name, email, message, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (name, email, message, datetime.utcnow().isoformat()),
            )
            db.commit()
            flash("Thanks for contacting us. We will reach out soon.", "success")

        return redirect(url_for("contact"))

    return render_template("contact.html")


# ---------- Admin routes ----------
@app.route("/fadak-admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin_logged_in"] = True
            flash("Welcome, admin.", "success")
            return redirect(url_for("admin_dashboard"))

        flash("Invalid username or password.", "danger")

    return render_template("admin_login.html")


@app.route("/fadak-admin/logout")
@admin_required
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("admin_login"))


@app.route("/fadak-admin/dashboard")
@admin_required
def admin_dashboard():
    db = get_db()
    appointments = db.execute(
        """
        SELECT a.*, c.name, c.email, c.phone
        FROM appointments a
        JOIN customers c ON a.customer_id = c.customer_id
        ORDER BY a.appointment_date DESC, a.appointment_time DESC
        """
    ).fetchall()
    vehicles = db.execute("SELECT * FROM vehicles ORDER BY vehicle_id DESC").fetchall()
    inquiries = db.execute(
        "SELECT * FROM inquiries ORDER BY created_at DESC"
    ).fetchall()

    def count_appts(status):
        return sum(1 for a in appointments if a["status"] == status)

    stats = {
        "appointments_total": len(appointments),
        "appointments_pending": count_appts("Pending"),
        "appointments_confirmed": count_appts("Confirmed"),
        "appointments_completed": count_appts("Completed"),
        "vehicles_total": len(vehicles),
        "vehicles_available": sum(1 for v in vehicles if v["status"] == "Available"),
        "vehicles_sold": sum(1 for v in vehicles if v["status"] == "Sold"),
        "inventory_value": sum(
            v["price"] for v in vehicles if v["status"] == "Available"
        ),
        "inquiries_total": len(inquiries),
        "inquiries_unread": sum(1 for i in inquiries if not i["is_read"]),
    }

    return render_template(
        "admin_dashboard.html",
        appointments=appointments,
        vehicles=vehicles,
        inquiries=inquiries,
        stats=stats,
    )


@app.route("/fadak-admin/appointments/<int:appointment_id>/delete", methods=["POST"])
@admin_required
def delete_appointment(appointment_id):
    db = get_db()
    db.execute("DELETE FROM appointments WHERE appointment_id = ?", (appointment_id,))
    db.commit()
    flash("Appointment deleted.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/fadak-admin/inquiries/<int:inquiry_id>/read", methods=["POST"])
@admin_required
def mark_inquiry_read(inquiry_id):
    db = get_db()
    db.execute("UPDATE inquiries SET is_read = 1 WHERE inquiry_id = ?", (inquiry_id,))
    db.commit()
    flash("Inquiry marked as read.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/fadak-admin/inquiries/<int:inquiry_id>/delete", methods=["POST"])
@admin_required
def delete_inquiry(inquiry_id):
    db = get_db()
    db.execute("DELETE FROM inquiries WHERE inquiry_id = ?", (inquiry_id,))
    db.commit()
    flash("Inquiry deleted.", "info")
    return redirect(url_for("admin_dashboard"))


@app.route("/fadak-admin/appointments/<int:appointment_id>/status", methods=["POST"])
@admin_required
def update_appointment_status(appointment_id):
    valid_statuses = {"Pending", "Confirmed", "Completed", "Cancelled"}
    new_status = request.form.get("status", "Pending")

    if new_status not in valid_statuses:
        flash("Invalid appointment status.", "danger")
        return redirect(url_for("admin_dashboard"))

    db = get_db()
    db.execute(
        "UPDATE appointments SET status = ? WHERE appointment_id = ?",
        (new_status, appointment_id),
    )
    db.commit()

    flash("Appointment status updated.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/fadak-admin/vehicles")
@admin_required
def admin_vehicles():
    db = get_db()
    vehicles = db.execute("SELECT * FROM vehicles ORDER BY vehicle_id DESC").fetchall()
    return render_template("admin_vehicles.html", vehicles=vehicles)


@app.route("/fadak-admin/vehicles/add", methods=["GET", "POST"])
@admin_required
def add_vehicle():
    if request.method == "POST":
        return save_vehicle_form()
    return render_template("admin_vehicle_form.html", vehicle=None, form_action=url_for("add_vehicle"))


@app.route("/fadak-admin/vehicles/<int:vehicle_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_vehicle(vehicle_id):
    db = get_db()
    vehicle = db.execute("SELECT * FROM vehicles WHERE vehicle_id = ?", (vehicle_id,)).fetchone()

    if vehicle is None:
        flash("Vehicle not found.", "danger")
        return redirect(url_for("admin_vehicles"))

    if request.method == "POST":
        return save_vehicle_form(vehicle_id=vehicle_id)

    return render_template(
        "admin_vehicle_form.html",
        vehicle=vehicle,
        form_action=url_for("edit_vehicle", vehicle_id=vehicle_id),
    )


@app.route("/fadak-admin/vehicles/<int:vehicle_id>/delete", methods=["POST"])
@admin_required
def delete_vehicle(vehicle_id):
    db = get_db()
    db.execute("DELETE FROM vehicles WHERE vehicle_id = ?", (vehicle_id,))
    db.commit()

    flash("Vehicle removed from inventory.", "info")
    return redirect(url_for("admin_vehicles"))


def save_vehicle_form(vehicle_id=None):
    """Shared add/edit vehicle handler."""
    db = get_db()

    year = parse_int(request.form.get("year"), None)
    make = request.form.get("make", "").strip()
    model = request.form.get("model", "").strip()
    mileage = parse_int(request.form.get("mileage"), None)
    price = parse_float(request.form.get("price"), None)
    condition = request.form.get("condition", "").strip()
    vin = request.form.get("vin", "").strip()
    description = request.form.get("description", "").strip()
    image_url = request.form.get("image_url", "").strip()
    status = request.form.get("status", "").strip()

    errors = []
    if not year:
        errors.append("Year is required.")
    if not make:
        errors.append("Make is required.")
    if not model:
        errors.append("Model is required.")
    if mileage is None:
        errors.append("Mileage is required.")
    if price is None:
        errors.append("Price is required.")
    if condition not in {"New", "Used", "Certified"}:
        errors.append("Condition must be New, Used, or Certified.")
    if status not in {"Available", "Sold"}:
        errors.append("Status must be Available or Sold.")

    if errors:
        for error in errors:
            flash(error, "danger")

        # Re-render form with entered values if validation fails.
        vehicle_data = {
            "vehicle_id": vehicle_id,
            "year": request.form.get("year", ""),
            "make": make,
            "model": model,
            "mileage": request.form.get("mileage", ""),
            "price": request.form.get("price", ""),
            "condition": condition,
            "vin": vin,
            "description": description,
            "image_url": image_url,
            "status": status,
        }
        action = url_for("add_vehicle") if vehicle_id is None else url_for("edit_vehicle", vehicle_id=vehicle_id)
        return render_template("admin_vehicle_form.html", vehicle=vehicle_data, form_action=action)

    if vehicle_id is None:
        db.execute(
            """
            INSERT INTO vehicles
            (year, make, model, mileage, price, condition, vin, description, image_url, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (year, make, model, mileage, price, condition, vin, description, image_url, status),
        )
        flash("Vehicle added successfully.", "success")
    else:
        db.execute(
            """
            UPDATE vehicles
            SET year = ?, make = ?, model = ?, mileage = ?, price = ?,
                condition = ?, vin = ?, description = ?, image_url = ?, status = ?
            WHERE vehicle_id = ?
            """,
            (year, make, model, mileage, price, condition, vin, description, image_url, status, vehicle_id),
        )
        flash("Vehicle updated successfully.", "success")

    db.commit()
    return redirect(url_for("admin_vehicles"))


# ---------- Error handlers ----------
@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", code=400,
                           message="Bad request. Your form session may have expired — please try again."), 400


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", code=404,
                           message="The page you are looking for could not be found."), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", code=500,
                           message="Something went wrong on our end. Please try again later."), 500


# Run once at import so `flask run` also creates/fixes the DB.
init_db()

if __name__ == "__main__":
    app.run(debug=DEBUG, host="127.0.0.1", port=int(os.environ.get("PORT", 5000)))
