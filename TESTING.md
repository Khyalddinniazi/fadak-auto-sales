# TESTING.md

## Test Environment
- OS: macOS / Windows / Linux
- Python: 3.10+
- Browser: Chrome, Edge, Firefox (latest)
- App URL: `http://127.0.0.1:5000`

## Functional Test Cases

1. **View services page**
   - Step: Open `/services`.
   - Expected: All services display with name, description, price, booking button, and the "Call for a quote" callout.

2. **Customer submits appointment (valid)**
   - Step: Open `/appointment`, fill all required fields, submit.
   - Expected: Success flash message appears and record is saved in database/admin dashboard.

3. **Customer submits appointment with "Other"**
   - Step: On `/appointment`, choose `Other (Call for a quote)` as the service type, submit.
   - Expected: Appointment saves with that service type and shows in the admin dashboard.

4. **Customer submits appointment (invalid/empty)**
   - Step: Submit form with missing required fields or a past date.
   - Expected: Validation errors appear; no invalid appointment is saved.

5. **Customer sends a contact message**
   - Step: Open `/contact`, fill the form, submit.
   - Expected: Success message; the inquiry appears in the admin dashboard.

6. **Admin login**
   - Step: Open `/fadak-admin/login`, use `admin / admin123` (local).
   - Expected: Redirect to admin dashboard.

7. **Admin updates appointment status**
   - Step: On `/fadak-admin/dashboard`, change an appointment status in dropdown.
   - Expected: Status updates to selected value and persists after reload.

8. **Admin adds a service**
   - Step: Go to `/fadak-admin/services` -> `Add New Service`, submit a valid form.
   - Expected: New service appears in the admin list and on the public Services page.

9. **Admin edits a service / changes price**
   - Step: Click `Edit` on a service, change the price, save.
   - Expected: Updated price appears in admin and on the public Services page.

10. **Admin deletes a service**
    - Step: Click `Delete` on a service and confirm.
    - Expected: Service removed from admin list and public Services page.

11. **Duplicate service name rejected**
    - Step: Add a service with a name that already exists.
    - Expected: A validation error is shown and no duplicate is created.

12. **Removed pages return 404**
    - Step: Visit `/inventory` or `/vehicles/1`.
    - Expected: Custom 404 page (inventory/vehicle features were removed).

13. **Responsive design**
    - Step: Resize browser to mobile width (<= 760px).
    - Expected: Navbar collapses to menu button; cards/forms remain readable and usable.
