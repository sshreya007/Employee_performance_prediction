from database.database import get_db
from auth.password_utils import hash_password, verify_password


def get_user(username: str) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    return dict(row) if row else None


def get_user_by_email(email: str) -> dict | None:
    db = get_db()
    row = db.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    return dict(row) if row else None


def create_user(full_name: str, username: str, email: str, password: str, role: str = "hr") -> bool:
    """Returns True on success, False if username/email already exists."""
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (full_name, username, email, password, role) VALUES (?,?,?,?,?)",
            (full_name, username, email, hash_password(password), role),
        )
        db.commit()
        return True
    except Exception:
        return False


def authenticate(username: str, password: str) -> dict | None:
    """Returns user dict if credentials are valid, else None."""
    user = get_user(username)
    if user and verify_password(password, user["password"]):
        return user
    return None


def update_profile(username: str, full_name: str, email: str) -> bool:
    db = get_db()
    try:
        db.execute(
            "UPDATE users SET full_name=?, email=? WHERE username=?",
            (full_name, email, username),
        )
        db.commit()
        return True
    except Exception:
        return False


def change_password(username: str, new_password: str) -> bool:
    db = get_db()
    try:
        db.execute(
            "UPDATE users SET password=? WHERE username=?",
            (hash_password(new_password), username),
        )
        db.commit()
        return True
    except Exception:
        return False
