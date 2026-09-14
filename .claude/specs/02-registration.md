# Spec: Registration

## Overview
This feature wires up real user registration for Spendly. Currently `/register` only renders `register.html` with no backend logic — submitting the form does nothing. This step adds the POST handler that validates input, checks for duplicate emails, hashes the password with `werkzeug`, and inserts a new row into the `users` table created in Step 1. Registration is the entry point that all future authenticated features (login, profile, expenses) depend on.

## Depends on
- Step 1 (Database Setup) — requires a working `get_db()`, `init_db()`, and the `users` table with `email` (unique) and `password_hash` columns.

## Routes
- GET /register – renders the registration form – public
- POST /register – validates input, creates the user, then redirects – public

## Validation rules
- `name`, `email`, `password` are required (reject empty/whitespace-only values)
- `email` must not already exist in `users` — on conflict, re-render `register.html` with an `error` message and the submitted values preserved in the form
- `password` minimum length of 8 characters
- On success: hash the password with `werkzeug.security.generate_password_hash`, insert the user via a parameterised `INSERT`, then redirect to `/login`

## Templates
- `register.html` already exists and extends `base.html` — reuse its existing form fields/markup, only adding the `error` rendering path already expected by the template
- No new templates required

## Always include
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables – never hardcode hex values
- All templates extend base.html

## Definition of done
- [ ] GET /register renders the form with no errors
- [ ] Submitting valid name/email/password creates a row in `users` with a hashed password (verify via sqlite3 CLI or a quick script — never a plaintext password)
- [ ] Submitting a duplicate email re-renders `register.html` with an error and does not insert a second row
- [ ] Submitting an empty field re-renders `register.html` with an error and does not insert a row
- [ ] Submitting a password under 8 characters re-renders `register.html` with an error and does not insert a row
- [ ] Successful registration redirects to /login
- [ ] All new queries use `?` placeholders (no string-formatted SQL)
- [ ] App starts and runs without errors after the change
