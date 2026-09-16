# Spec: Profile Page

## Overview
This feature builds out the real `/profile` page for Spendly. Currently `/profile` returns the placeholder string `"Profile page — coming in Step 4"`. This is the page users land on immediately after a successful login (see Step 3), so it is effectively the app's post-login home for now. This step replaces the placeholder with a real page that shows the logged-in user's account details and a lightweight read-only snapshot of their spending, using the `users` and `expenses` tables already created in Step 1. It does not add any expense creation/editing/deleting — that's Steps 7–9.

## Depends on
- Step 1 (Database Setup) — requires `get_db()` and the `users` / `expenses` tables.
- Step 3 (Login and Logout) — requires `session['user_id']` to identify the logged-in user; `/profile` is reached after a successful login.

## Routes
- `GET /profile` – renders the logged-in user's profile – logged in only. If `session.get('user_id')` is not set, redirect to `/login` (no flash message needed — this mirrors the "no hard enforcement" note in Step 3, but a page that displays personal data should not render for a logged-out visitor).

No POST route in this step — profile editing (name/email/password changes) is out of scope and not listed among the placeholder routes in `app.py`.

## Database changes
No schema changes. Uses existing tables read-only:
- `users` — fetch the current user's `name`, `email`, `created_at` via `SELECT ... WHERE id = ?` using `session['user_id']`.
- `expenses` — fetch a simple aggregate snapshot for the current user only (read-only `SELECT`, no writes): total number of expenses logged, and total amount spent. Both scoped with `WHERE user_id = ?`.

## Templates
- **Create:** `templates/profile.html` — extends `base.html`.
- **Modify:** none. `base.html` nav already conditionally shows "Logout" when `session.get('user_id')` is set (done in Step 3) — no changes needed there.

### `profile.html` structure
- Page header: user's name as the title, email as a subtitle, and a "Member since <Month Year>" line (formatted from `created_at`).
- An "at a glance" section with two stat cards (reusing the existing `.stat-tile` / `.stat-value` / `.stat-label` pattern already defined in `static/css/style.css`): "Expenses logged" (count) and "Total spent" (sum, formatted as currency).
- A "Log out" button (`href="{{ url_for('logout') }}"`, styled with the existing `.btn-ghost` or `.btn-accent` class) as a secondary way to sign out from the page itself.

## Files to change
- `app.py` — replace the placeholder `profile()` view with the real implementation described above.

## Files to create
- `templates/profile.html`

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (n/a here — no password handling in this step)
- Use CSS variables – never hardcode hex values
- All templates extend `base.html`
- Reuse existing CSS classes (`.stat-tile`, `.stat-label`, `.stat-value`, `.btn-ghost`, `.btn-accent`, `.auth-card`-style card patterns) before inventing new ones — only add new CSS if nothing existing fits, matching the frontend-design skill's "anchor to the existing design" guidance.
- Do not add expense list/add/edit/delete UI — that's Steps 7–9.

## Definition of done
- [ ] Visiting `/profile` while logged out redirects to `/login`
- [ ] Visiting `/profile` while logged in (e.g. as the seeded demo user, `demo@spendly.com` / `demo123`) renders the user's name, email, and member-since date
- [ ] The "Expenses logged" stat matches `COUNT(*)` of the demo user's rows in `expenses` (8 after seeding)
- [ ] The "Total spent" stat matches `SUM(amount)` of the demo user's rows in `expenses`
- [ ] The page includes a working "Log out" control that clears the session and redirects to the landing page
- [ ] The page extends `base.html` and uses only existing CSS variables/classes (no hardcoded hex values)
- [ ] All new queries use `?` placeholders (no string-formatted SQL)
- [ ] App starts and runs without errors after the change
