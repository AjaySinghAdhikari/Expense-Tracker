# Spec: Login and Logout

## Overview
This feature wires up real authentication for Spendly. Currently `/login` only renders `login.html` with no backend logic, and `/logout` returns the placeholder string `"Logout — coming in Step 3"`. This step adds the POST handler that verifies a user's email/password against the `users` table (created in Step 1, populated by Step 2 registration), establishes a logged-in session using Flask's built-in cookie-based `session`, and adds a working logout that clears it. Session state introduced here (`session['user_id']`) is the foundation later steps (Profile, Expenses) will depend on to identify the current user and gate access.

## Depends on
- Step 1 (Database Setup) — requires a working `get_db()` and the `users` table with `email` (unique) and `password_hash` columns.
- Step 2 (Registration) — requires at least one row in `users` with a `werkzeug`-hashed password to log in with (also satisfied by the seeded demo user, `demo@spendly.com` / `demo123`).

## Routes
- `GET /login` – renders the login form – public (already exists, unchanged)
- `POST /login` – validates email/password against `users`, starts a session on success – public
- `GET /logout` – clears the session, redirects to the landing page – logged in (no hard enforcement needed; clearing an empty session is a harmless no-op if hit while logged out)

## Database changes
No database changes. Auth state is stored in Flask's signed session cookie (`session['user_id']`), not a server-side table.

Note: Flask's `session` requires `app.secret_key` to be set. `app.py` does not currently set one — this must be added (e.g. read from an environment variable with a dev-only fallback) for sessions to work at all.

## Templates
- **Create:** none
- **Modify:**
  - `templates/base.html` – the nav currently always shows "Sign in" / "Get started" regardless of auth state. Update it to check `session.get('user_id')` (Flask templates have implicit access to `session`) and conditionally show a "Logout" link (`{{ url_for('logout') }}`) in place of "Sign in" / "Get started" when logged in.
  - `templates/login.html` – no structural changes; it already POSTs to `/login` and renders an `error` variable on failure, matching the pattern used by `register.html`.

## Files to change
- `app.py` – set `app.secret_key`; implement `POST /login` (validate credentials, set session, redirect); implement `GET /logout` (clear session, redirect)
- `templates/base.html` – conditional nav based on session state

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug — use `werkzeug.security.check_password_hash` to verify on login (never compare plaintext)
- Use CSS variables – never hardcode hex values
- All templates extend `base.html`
- On invalid login (unknown email, or wrong password), re-render `login.html` with a single generic `error` message (e.g. "Invalid email or password.") — do not reveal whether the email exists, to avoid user enumeration
- Redirect a successful login to `/profile` (the Step 4 placeholder route) — this is the natural post-login destination even though its content isn't built yet

## Definition of done
- [ ] GET /login renders the form with no errors
- [ ] Submitting the seeded demo credentials (`demo@spendly.com` / `demo123`) logs in and redirects to `/profile`
- [ ] Submitting a correct email with the wrong password re-renders `login.html` with a generic error and does not start a session
- [ ] Submitting an email that doesn't exist re-renders `login.html` with the same generic error and does not start a session
- [ ] After a successful login, the nav in `base.html` shows a "Logout" link instead of "Sign in" / "Get started"
- [ ] Visiting /logout while logged in clears the session and redirects to the landing page, and the nav reverts to showing "Sign in" / "Get started"
- [ ] Visiting /logout while logged out does not error
- [ ] All new queries use `?` placeholders (no string-formatted SQL)
- [ ] App starts and runs without errors after the change
