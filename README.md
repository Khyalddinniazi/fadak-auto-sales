# Fadak Auto Sales — Auto Service Center 🚗🔧

A full-stack web application for a real auto service center, built with **Python + Flask** and deployed to production. Customers can browse services, book appointments online, and contact the shop, while the owner manages everything through a secure, password-protected admin dashboard.

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white">
  <img alt="Flask" src="https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white">
  <img alt="SQLite" src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white">
  <img alt="Gunicorn" src="https://img.shields.io/badge/Gunicorn-Production-499848?logo=gunicorn&logoColor=white">
  <img alt="Deployed on Render" src="https://img.shields.io/badge/Deployed-Render-46E3B7">
</p>

> **🔗 Live Demo:** https://fadak-auto-sales.onrender.com
> _(Free hosting — the first load after inactivity may take ~30–50s to wake up.)_

---

## 📌 Overview

This project is a complete, production-deployed web app — not just a tutorial demo. It covers the full lifecycle: a polished public-facing website, a secure back-office admin panel, a relational database, server-side validation, and a real cloud deployment with environment-based configuration.

It has two sides:

- **Public website** — customers explore the service menu, book appointments, and send messages.
- **Admin dashboard** — the owner logs in privately to manage services and pricing, track appointments, and read customer inquiries.

---

## ✨ Key Features

### Customer-facing
- Responsive, modern UI that works on desktop and mobile
- Service menu with live pricing, loaded dynamically from the database
- Online appointment booking with full validation (no past-date bookings)
- **"Other — Call for a quote"** option for services not on the menu
- Contact form that saves inquiries for the owner to follow up on

### Admin dashboard (secure)
- Live business stats: appointments by status, services offered, unread inquiries
- **Full service management (CRUD):** add, edit, delete, and change prices
- Appointment workflow management (update status, delete)
- Customer inquiry inbox (mark read / delete)

### Engineering & security
- **Hashed admin password** (Werkzeug) — never stored in plain text
- **CSRF protection** on every form
- **Security headers** (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`) + hardened session cookies
- **Environment-based secrets** — credentials and keys are never committed to the repo
- Custom **404 / 500 error pages**
- Server-side **and** client-side input validation

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Templating | Jinja2 |
| Database | SQLite (schema designed for easy migration to Postgres/MySQL) |
| Frontend | HTML5, CSS3, vanilla JavaScript |
| Auth/Security | Werkzeug password hashing, custom CSRF tokens |
| Production server | Gunicorn |
| Hosting / CI | Render (auto-deploys from GitHub) |

---

## 🧱 Architecture

The app follows a clean MVC-style separation:

- **Routes & logic** live in `app.py` (request handling, validation, auth, DB access).
- **Views** are Jinja2 templates in `templates/` that render live data.
- **Data** is stored in SQLite, with the schema auto-created on startup.

```
Browser ──▶ Flask routes (app.py) ──▶ SQLite (services, appointments, customers, inquiries)
                  │
                  └──▶ Jinja2 templates ──▶ rendered HTML ──▶ Browser
```

### Database schema
- **`customers`** — `customer_id` (PK), `name`, `email`, `phone`
- **`appointments`** — `appointment_id` (PK), `customer_id` (FK), vehicle info, `service_type`, date/time, `status`, `created_at`
- **`services`** — `service_id` (PK), `service_name` (unique), `description`, `estimated_price`
- **`inquiries`** — `inquiry_id` (PK), `name`, `email`, `message`, `is_read`, `created_at`

Full SQL in [`database/schema.sql`](database/schema.sql).

---

## 📷 Screenshots

> _Add screenshots here to showcase the UI (home, services, booking, admin dashboard)._

| Home | Admin Dashboard |
|------|-----------------|
| _(screenshot)_ | _(screenshot)_ |

---

## 🚀 Run It Locally

**Prerequisites:** Python 3.11+

```bash
# 1. Clone the repo
git clone https://github.com/Khyalddinniazi/fadak-auto-sales.git
cd fadak-auto-sales

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run in development mode
FLASK_DEBUG=1 python app.py      # Windows (cmd): set FLASK_DEBUG=1 && python app.py
```

Then open **http://127.0.0.1:5000**

The SQLite database is created automatically on first run, pre-seeded with a starter service menu.

**Local admin login:** `admin` / `admin123` → at `/fadak-admin/login`

---

## ☁️ Deployment

The app is production-ready and deployed on **Render** via the included [`render.yaml`](render.yaml) blueprint and [`Procfile`](Procfile) (Gunicorn).

In production, these are set as environment variables (never in code):

| Variable | Purpose |
|---|---|
| `SECRET_KEY` | Signs user sessions (required when not in debug) |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | Admin login credentials (password is hashed at runtime) |
| `FLASK_DEBUG` | `0` in production |

The app intentionally **refuses to start without a `SECRET_KEY`** in production — a safeguard against insecure deploys.

---

## 📂 Project Structure

```
fadak-auto-sales/
├── app.py              # Routes, logic, security, DB setup
├── seed_data.py        # Initial service menu
├── requirements.txt    # Dependencies
├── Procfile            # Gunicorn start command (production)
├── render.yaml         # Render deployment blueprint
├── .env.example        # Environment variable template
├── database/
│   └── schema.sql      # Reference SQL schema
├── templates/          # Jinja2 HTML templates
└── static/             # CSS, JavaScript, images
```

---

## 🔮 Possible Future Enhancements

- In-dashboard "Change Password" page and multiple staff accounts with roles
- Email/SMS notifications for new bookings and inquiries
- Migrate to PostgreSQL for higher-traffic, multi-instance hosting
- Pagination, sorting, and search on admin tables

---

## 👤 Author

Built by **Khyalddin Niazi**. Feedback and contributions welcome.
