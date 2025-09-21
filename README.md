# Giano - Smart Digital Clocking (Demo)

This is a minimal demo Django project that demonstrates a kiosk/mobile flow for attendance:
- Kiosk generates a short single-use token (shown in the kiosk view).
- Mobile user opens the mobile confirm URL and taps Confirm.
- The kiosk polls the server and updates when the session is verified.
- AttendanceRecord saves a simple record in SQLite.

## Quickstart (local)

1. Create virtualenv and install requirements:
   python -m venv env
   source env/bin/activate
   pip install -r requirements.txt

2. Run migrations and create superuser:
   python manage.py migrate
   python manage.py createsuperuser

3. Run development server:
   python manage.py runserver

4. Open http://127.0.0.1:8000/ for kiosk view.
   Visit the mobile URL shown on kiosk to confirm.

## Notes
- This is a demo skeleton. For production you must:
  - Use authentication on mobile confirm.
  - Replace token display with a QR code (e.g. generate QR on kiosk using a JS QR lib).
  - Add session expiry, hardening, logging, HTTPS, and proper user management.
