# AutoCare Dealership & Service Center

A full-stack Flask web application for a small dealership and mechanic shop. Customers can browse cars, review services, book appointments, and contact the business. The admin can log in to manage appointments and vehicle inventory.

## Features

- Clean, responsive dealership-style frontend (desktop + mobile)
- Home page with featured vehicles, services, and trust badges
- Inventory page with filters (search, price range, year, condition)
- Vehicle detail page with pricing, mileage, VIN placeholder, and contact actions
- Services page with estimated pricing and booking links
- Appointment booking with validation and database storage
- Contact page with business details and contact form
- Secure admin login (hashed password, env-configurable credentials)
- Admin dashboard with live stats (appointments by status, inventory value, unread inquiries)
- Admin appointment management (update status, delete)
- Customer inquiries captured from the contact form and managed in the dashboard
- Admin vehicle management (add, edit, delete, mark Available/Sold)
- CSRF protection on all forms, security headers, and custom error pages

## Technologies Used

- Frontend: HTML5, CSS3, JavaScript
- Backend: Python 3 + Flask
- Database: SQLite (with schema structured for easy migration to MySQL later)

## Database Design Summary

### `customers`
- `customer_id` (PK)
- `name`, `email`, `phone`

### `appointments`
- `appointment_id` (PK)
- `customer_id` (FK -> customers)
- `vehicle_make`, `vehicle_model`, `vehicle_year`
- `service_type`, `appointment_date`, `appointment_time`
- `notes`, `status`, `created_at`

### `vehicles`
- `vehicle_id` (PK)
- `year`, `make`, `model`, `mileage`, `price`
- `condition`, `vin`, `description`, `image_url`, `status`

### `services`
- `service_id` (PK)
- `service_name`, `description`, `estimated_price`

### `inquiries`
- `inquiry_id` (PK)
- `name`, `email`, `message`, `is_read`, `created_at`

## Local Setup and Run

1. Open terminal and move into project folder:
   ```bash
   cd AutoCare-Dealership-Service-Center
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open your browser at:
   - [http://127.0.0.1:5000](http://127.0.0.1:5000)

The SQLite database file is automatically created at `database/mechanic_shop.db` when you first run the app.

## Demo Admin Login (development only)

- Username: `admin`
- Password: `admin123`

These defaults only apply when no `ADMIN_USERNAME` / `ADMIN_PASSWORD` environment
variables are set. The demo credentials hint on the login page is hidden unless
`FLASK_DEBUG=1`.

## Going Live (Production Deployment)

This app is configured for a production deployment. Before going live:

1. Create a `.env` file from the template and set real values:
   ```bash
   cp .env.example .env
   ```
   - `SECRET_KEY` — generate one with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `ADMIN_USERNAME` / `ADMIN_PASSWORD` — your real admin credentials
   - Leave `FLASK_DEBUG=0` (the app refuses to start without a `SECRET_KEY` when debug is off)

2. Run with a production WSGI server (Gunicorn):
   ```bash
   gunicorn app:app --bind 0.0.0.0:8000 --workers 3
   ```
   A `Procfile` is included for platforms like Render, Railway, Heroku, or Fly.io.

3. Serve behind HTTPS. The session cookie is marked `Secure` automatically when
   `FLASK_DEBUG` is off, so the app must be reached over HTTPS in production.

### Security features included
- Admin password is hashed (never compared in plain text)
- CSRF tokens on every state-changing form
- Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`)
- Hardened session cookie (`HttpOnly`, `SameSite=Lax`, `Secure` in production)
- Secret key required from the environment in production

## Screenshots

Add screenshots here after running the project locally:
- Home page
- Inventory page
- Vehicle details page
- Appointment page
- Admin dashboard

## Future Improvements

- Add image upload support for vehicle photos
- Integrate MySQL/PostgreSQL for higher-traffic deployments
- Add email notifications for appointment confirmations and inquiries
- Add pagination and sorting to the inventory and admin tables
- Multi-user admin accounts with roles
