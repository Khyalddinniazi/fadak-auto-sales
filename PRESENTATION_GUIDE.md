# Fadak Auto Sales — Project & Presentation Guide

A complete companion for running and presenting this project. Read it top to
bottom once before the presentation, then keep the "Run It" and "Demo Script"
sections open during the demo.

---

## 1. What This Project Is (the 30-second pitch)

**Fadak Auto Sales** is a full-stack web application for an auto service center.
It has two sides:

- **The public website** — where customers view service pricing, book a service
  appointment (including an "Other / Call for a quote" option), and contact the
  business.
- **The admin dashboard** — a private, password-protected area where the owner
  manages the service menu (add/edit/delete and change prices), appointments,
  and customer messages.

**Built with:** Python + Flask (backend), SQLite (database), and HTML / CSS /
JavaScript (frontend).

---

## 1.5 Technologies Used — Explained Simply

This project uses a few core technologies, and each one has a clear job. In
plain words:

- **Python** is the programming language everything is written in. Think of it
  as the language we use to give the computer instructions. It's popular because
  it's readable and powerful, and it handles all the "thinking" behind the
  scenes — like checking if a form was filled out correctly or pulling the right
  services from storage.

- **Flask** is a *web framework* for Python — basically a toolkit that turns our
  Python code into a real website. Its main job is to listen for requests (like
  "show me the inventory page") and send back the right web page in response.
  When someone clicks a link or submits a form, Flask is the part that decides
  what happens next. It's called "lightweight" because it's simple and doesn't
  force a lot of extra structure on you.

- **SQLite** is the *database* — the place where all the information is stored
  permanently: the cars, customer details, appointments, and contact messages.
  It's a single file (`database/mechanic_shop.db`) that lives inside the
  project, so there's no separate database server to install. When a customer
  books an appointment, SQLite is where that booking is saved so it's still
  there later when the owner opens the admin dashboard.

- **Jinja2** (comes built into Flask) is the *templating engine*. It lets us
  build HTML pages that can show live data — for example, the same services
  template displays whatever services are currently in the database, instead of
  us writing each one by hand.

- **HTML, CSS, and JavaScript** are the frontend — the part the user actually
  sees and clicks. **HTML** is the structure (headings, buttons, forms),
  **CSS** is the styling (colors, layout, the modern look), and **JavaScript**
  adds small interactive touches (like the mobile menu and the fade-in
  animations).

- **Werkzeug** (also bundled with Flask) handles security behind the scenes,
  including scrambling ("hashing") the admin password so it's never stored as
  plain text.

- **Gunicorn** is a *production web server*. We don't use it for the local demo,
  but it's what would run the app on a real live website to handle many visitors
  reliably.

### What happens when you run the app (and what "http://127.0.0.1:5000" means)

When you run `python app.py`, Flask starts a small **web server** on your own
computer. A web server is just a program that waits for a browser to ask for a
page and then sends it back. In simple terms, your laptop is briefly *both* the
website's host *and* the visitor.

The address **`http://127.0.0.1:5000`** breaks down like this:

- **`http://`** — the language browsers and servers use to talk to each other
  (HyperText Transfer Protocol). It's how the request for a page and the page
  itself travel back and forth.
- **`127.0.0.1`** — a special address that always means *"this same computer."*
  It's also nicknamed **`localhost`**. So the website is only running on your
  machine, not on the internet — perfect for a private demo.
- **`5000`** — the *port number*, like a specific door on your computer that the
  app is listening behind. Flask uses 5000 by default.

So when you type that address into your browser, you're saying *"ask the app
running on my own computer, behind door 5000, to show me its home page."* Flask
receives that, runs the matching Python code, pulls any needed data from SQLite,
fills in the HTML template, and sends the finished page back to your browser.

> **About HTTPS (the secure padlock):** Locally you'll see `http`, not `https`,
> and that's completely fine for a demo on your own computer. **HTTPS** is the
> encrypted, secure version of HTTP — the padlock you see on real websites. It's
> added automatically by the hosting provider once the site is live on the
> internet, so customers' information travels safely. We don't need it for the
> local presentation because nothing is leaving your laptop.

---

## 2. How the Project Is Organized

```
AutoCare-Dealership-Service-Center/
├── app.py              # The brain: all pages, logic, security, database setup
├── seed_data.py        # Starter data: the initial service menu
├── requirements.txt    # The Python packages the app needs
├── database/           # The SQLite database file lives here (auto-created)
├── templates/          # The HTML pages (what the user sees)
│   ├── base.html              # Shared layout: navbar + footer
│   ├── index.html             # Home page
│   ├── services.html          # Service menu
│   ├── appointment.html       # Booking form
│   ├── contact.html           # Contact page
│   ├── error.html             # 404 / 500 error page
│   └── admin_*.html           # Admin login, dashboard, service management
└── static/             # CSS, JavaScript, and images
    ├── css/style.css
    ├── js/script.js
    └── images/
```

**The mental model:** `app.py` decides *what* to show and *what* data to load,
the `templates/` decide *how* it looks, and the `database/` stores everything
(cars, appointments, messages).

---

## 3. Getting the Project Onto a Windows Laptop

Pick **one** of these two ways.

### Option A — Copy the folder (simplest)
1. Zip the whole `AutoCare-Dealership-Service-Center` folder and send it
   (email, USB, Google Drive, etc.).
2. On the Windows laptop, **extract** the zip to somewhere easy like the
   Desktop.
3. **Important:** if a `.venv` folder is inside the zip, **delete it** after
   extracting — it was built for Mac and won't work on Windows. A fresh one is
   created in the setup steps below.

### Option B — GitHub (cleaner, if you use git)
1. Push the project to a GitHub repository.
2. On the Windows laptop: `git clone <your-repo-url>`

---

## 4. One-Time Setup on Windows

### Step 1 — Install Python
1. Go to <https://www.python.org/downloads/> and download Python 3.11 or newer.
2. Run the installer and **CHECK the box that says "Add Python to PATH"**
   (this is the most common thing people miss).
3. Click "Install Now".

Verify it worked — open **Command Prompt** (search "cmd" in the Start menu)
and type:
```cmd
python --version
```
You should see something like `Python 3.12.x`.

### Step 2 — Open the project folder in a terminal
In Command Prompt, move into the project folder. For example, if it's on the
Desktop:
```cmd
cd %USERPROFILE%\Desktop\AutoCare-Dealership-Service-Center
```

### Step 3 — Create and activate a virtual environment
A "virtual environment" keeps this project's packages separate from the rest of
the computer.
```cmd
python -m venv .venv
.venv\Scripts\activate
```
After activating, your prompt will start with `(.venv)`.

> If using **PowerShell** instead of Command Prompt and activation is blocked,
> run this once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` then
> `.venv\Scripts\Activate.ps1`.

### Step 4 — Install the required packages
```cmd
pip install -r requirements.txt
```

That's the full setup. You only do Steps 1–4 **once**.

---

## 5. Running the App (do this every time you present)

The app has a safety feature: it won't start in "production mode" without a
secret key. For a local demo, we turn on **development mode**, which skips that.

**In Command Prompt (cmd):**
```cmd
.venv\Scripts\activate
set FLASK_DEBUG=1
python app.py
```

**In PowerShell:**
```powershell
.venv\Scripts\activate
$env:FLASK_DEBUG = "1"
python app.py
```

You'll see a line like:
```
* Running on http://127.0.0.1:5000
```

Now open a browser and go to: **http://127.0.0.1:5000**

> **Note about the port:** On Windows, port 5000 is normally free, so the link
> above works. (On Macs it's often taken, which is why earlier we used port
> 8000 — that detail does not apply to Windows.)

**To stop the app:** click in the terminal window and press **Ctrl + C**.

---

## 6. Logging Into the Admin Dashboard

The admin area is **not linked anywhere on the public site** (so customers can't
find it). You reach it directly by typing the URL:

- Admin login: **http://127.0.0.1:5000/fadak-admin/login**
- Demo username: `admin`
- Demo password: `admin123`

After logging in you'll see the dashboard with stats, appointments, customer
inquiries, and a link to manage vehicles.

> These demo credentials are **for the local presentation only**. On a real live
> website, the owner sets a private username and password (see Section 9).

---

## 7. Demo Script — Presenting From Start to Finish

Follow this order during the live demo. Suggested talking points are in
*italics*.

**1. Home page (`/`)**
- *"This is the landing page. It has a video banner, the most popular services
  pulled live from the database, and trust badges."*
- Click **View Services** or **Book Service** to move into the site.

**2. Services page (`/services`)**
- *"The shop offers a full menu of services, each with a description and price,
  all loaded from the database. If a customer needs something not listed, there's
  a 'Call for a quote' callout right here."*

**3. Book an appointment (`/appointment`)**
- Fill out the form and submit.
- *"When a customer books, the details are validated and saved to the database.
  Notice you can't pick a date in the past, and there's an 'Other (Call for a
  quote)' option for anything not on the menu."*
- A green success message confirms it saved.

**4. Contact form (`/contact`)**
- Fill it out and submit.
- *"Customer messages are stored so the owner can follow up later."*

**5. Admin dashboard (`/fadak-admin/login`)** — the highlight
- Log in with `admin` / `admin123`.
- *"This is the private owner dashboard. At the top are live stats — how many
  appointments are pending, how many services are offered, and unread messages."*
- Show the **appointment you just booked** appearing in the list.
- Change its status from "Pending" to "Confirmed" — *"the owner manages the
  workflow right here."*
- Scroll to **Customer Inquiries** and show the message you just sent.
- Go to **Manage Services** → **Add New Service** (or edit one and change its
  price), then show it instantly updates on the public Services page. Delete it
  to show full control.

**6. Wrap-up**
- *"So the whole system connects: customers interact on the public site, and
  everything flows into a secure admin dashboard the owner uses to run the
  business — including full control over the services and pricing."*

---

## 8. Technical Talking Points (for questions)

Be ready for these — they make the project sound professional:

- **Architecture:** *"It's a Flask web app following the MVC idea — routes in
  `app.py` handle logic, Jinja2 templates handle the display, and SQLite stores
  the data."*
- **Database:** *"Four main tables — services, customers, appointments, and
  inquiries — linked with proper relationships (an appointment belongs to a
  customer)."*
- **Security (this impresses):**
  - Admin passwords are **hashed**, never stored as plain text.
  - Every form has **CSRF protection** to block fake/forged submissions.
  - **Security headers** and a hardened session cookie.
  - Credentials and the secret key come from **environment variables** in
    production, not the code.
- **Validation:** *"Forms are checked on both the browser side and the server
  side — for example, you can't book a date in the past or submit an empty
  appointment."*
- **Production-ready:** *"It includes a Procfile and Gunicorn so it can be
  deployed to a real host like Render or Railway."*

---

## 9. (Reference) How It Goes Live for Real

Not needed for the presentation, but good to know if asked *"how would this go
online?"*:

1. Push the code to a host like **Render**, **Railway**, or **Heroku**.
2. In the host's **Environment Variables** settings, set:
   - `SECRET_KEY` — a long random string
   - `ADMIN_USERNAME` and `ADMIN_PASSWORD` — the owner's real login
   - `FLASK_DEBUG=0`
3. The host runs it with Gunicorn (using the included `Procfile`).
4. The owner logs in at `your-domain.com/fadak-admin/login` with the credentials
   set in step 2. **This is how the owner "creates" the admin password** — no
   code editing required.

---

## 10. Troubleshooting

| Problem | Fix |
|---|---|
| `'python' is not recognized` | Python isn't on PATH. Reinstall and check "Add Python to PATH". |
| App stops with a `SECRET_KEY` error | You forgot to set `FLASK_DEBUG=1` before `python app.py`. |
| `pip install` fails | Make sure the venv is active (prompt shows `(.venv)`) and you have internet. |
| Page won't load in browser | Confirm the terminal still shows the app running, and use `http://127.0.0.1:5000`. |
| Car images don't show | You need an internet connection — the demo photos load from the web. |
| Port 5000 busy | Run `set FLASK_DEBUG=1 && set PORT=8000 && python app.py`, then use port 8000. |

---

## Quick Reference Card

**Setup (once):**
```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Run (every time):**
```cmd
.venv\Scripts\activate
set FLASK_DEBUG=1
python app.py
```

**Open:** http://127.0.0.1:5000
**Admin:** http://127.0.0.1:5000/fadak-admin/login  →  `admin` / `admin123`
**Stop:** Ctrl + C in the terminal
