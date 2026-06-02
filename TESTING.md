# TESTING.md

## Test Environment
- OS: macOS / Windows / Linux
- Python: 3.10+
- Browser: Chrome, Edge, Firefox (latest)
- App URL: `http://127.0.0.1:5000`

## Functional Test Cases

1. **Customer views inventory**
   - Step: Open `/inventory`
   - Expected: Vehicle cards load from database with price, year, make, model, status.

2. **Customer filters inventory**
   - Step: On `/inventory`, enter make/model, price range, year, or condition.
   - Expected: Results update and only matching vehicles are shown.

3. **Customer views vehicle details**
   - Step: Click `View Details` on any vehicle card.
   - Expected: Vehicle details page shows full information, VIN placeholder, and action buttons.

4. **Customer submits appointment (valid)**
   - Step: Open `/appointment`, fill all required fields, submit.
   - Expected: Success flash message appears and record is saved in database/admin dashboard.

5. **Customer submits appointment (invalid/empty)**
   - Step: Submit form with missing required fields.
   - Expected: Validation errors appear; no invalid appointment is saved.

6. **View services page**
   - Step: Open `/services`.
   - Expected: All services display with name, description, estimated price, and booking button.

7. **Admin login**
   - Step: Open `/fadak-admin/login`, use `admin / admin123`.
   - Expected: Redirect to admin dashboard.

8. **Admin updates appointment status**
   - Step: On `/fadak-admin/dashboard`, change an appointment status in dropdown.
   - Expected: Status updates to selected value and persists after reload.

9. **Admin adds vehicle**
   - Step: Go to `/fadak-admin/vehicles` -> `Add New Vehicle`, submit valid form.
   - Expected: New vehicle appears in admin vehicles table and public inventory.

10. **Admin edits vehicle**
    - Step: Click `Edit` on vehicle, change values, save.
    - Expected: Updated values appear in admin and public pages.

11. **Admin deletes vehicle**
    - Step: Click `Delete` on vehicle and confirm.
    - Expected: Vehicle removed from admin list and inventory page.

12. **Responsive design**
    - Step: Resize browser to mobile width (<= 760px).
    - Expected: Navbar collapses to menu button; cards/forms remain readable and usable.
