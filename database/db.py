import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "spendly.db")

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    demo_password_hash = generate_password_hash("demo123")
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", demo_password_hash),
    )
    user_id = cur.lastrowid

    today = date.today()
    sample_expenses = [
        (user_id, 24.50, "Food", f"{today:%Y-%m}-02", "Groceries"),
        (user_id, 15.00, "Transport", f"{today:%Y-%m}-04", "Bus pass top-up"),
        (user_id, 89.99, "Bills", f"{today:%Y-%m}-06", "Electricity bill"),
        (user_id, 60.00, "Health", f"{today:%Y-%m}-09", "Pharmacy"),
        (user_id, 40.00, "Entertainment", f"{today:%Y-%m}-12", "Movie night"),
        (user_id, 75.25, "Shopping", f"{today:%Y-%m}-15", "New shoes"),
        (user_id, 10.00, "Other", f"{today:%Y-%m}-18", "Miscellaneous"),
        (user_id, 32.40, "Food", f"{today:%Y-%m}-21", "Dinner out"),
    ]
    cur.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    seed_db()
    print(f"Database initialized at {DB_PATH}")
