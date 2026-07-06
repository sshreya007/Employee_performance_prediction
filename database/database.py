import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables and seed demo accounts if they don't exist."""
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name  TEXT    NOT NULL,
            username   TEXT    UNIQUE NOT NULL,
            email      TEXT    UNIQUE NOT NULL,
            password   TEXT    NOT NULL,
            role       TEXT    NOT NULL DEFAULT 'hr',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS predictions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            username     TEXT NOT NULL,
            employee_name TEXT,
            department   TEXT,
            job_role     TEXT,
            input_data   TEXT,
            prediction   INTEGER,
            confidence   REAL,
            created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    db.commit()

    # Seed demo users (ignore if already exist)
    import hashlib
    def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
    demo_users = [
        ("Admin HR",    "admin",     "admin@company.com",  "admin123", "admin"),
        ("HR Manager",  "hrmanager", "hr@company.com",     "hr1234",   "hr"),
    ]
    for full_name, username, email, pwd, role in demo_users:
        try:
            db.execute(
                "INSERT INTO users (full_name,username,email,password,role) VALUES (?,?,?,?,?)",
                (full_name, username, email, hash_password(pwd), role),
            )
        except sqlite3.IntegrityError:
            pass
    db.commit()
