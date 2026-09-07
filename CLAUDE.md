# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a teaching project: a Flask expense-tracker app called **Spendly**, built incrementally in numbered "Steps" (a student curriculum). Much of the app is intentionally unimplemented — routes return placeholder strings like `"Logout — coming in Step 3"`, and `database/db.py` is currently just a spec comment describing functions to write, not working code. When asked to implement a feature, check `app.py` and `database/db.py` for step markers/comments indicating what that step expects before writing code, and follow the existing code style rather than jumping ahead to unrelated future steps.

## Commands

- Run the dev server: `python app.py` (Flask runs on port 5001, debug mode on)
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest`
- Run a single test: `pytest path/to/test_file.py::test_name`

There is no lint/format/build tooling configured in this repo.

## Architecture

- **`app.py`** — single-file Flask app defining all routes. No blueprints; new routes are added directly here.
- **`database/db.py`** — intended to hold `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (creates tables with `CREATE TABLE IF NOT EXISTS`), and `seed_db()` (sample data for dev). The actual SQLite file (`expense_tracker.db`) is gitignored and created locally.
- **`templates/`** — Jinja2 templates. `base.html` is the shared layout (nav/footer, loads `static/css/style.css` and `static/js/main.js`) and defines `title`, `head`, `content`, `scripts` blocks that page templates extend.
- **`static/`** — `css/style.css` (all styling) and `js/main.js`.
- Auth forms (`login.html`, `register.html`) POST to `/login` and `/register` respectively and render an `error` template variable on failure — no auth logic is wired up yet.
- Route naming maps directly to template names (e.g. `landing()` → `landing.html`), and `url_for()` is used throughout templates for links — keep new routes/templates consistent with this pattern.
