-- SQLite schema and seed data for AutoCare Dealership & Service Center.
-- This file mirrors the schema created by app.py init_db().

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
