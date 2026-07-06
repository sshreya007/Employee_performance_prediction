import re


def valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


def valid_password(password: str) -> tuple[bool, str]:
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    return True, ""


def validate_signup(full_name, username, email, password, confirm, terms) -> list[str]:
    errors = []
    if not all([full_name, username, email, password, confirm]):
        errors.append("All fields are required.")
    if password and len(password) < 6:
        errors.append("Password must be at least 6 characters.")
    if password != confirm:
        errors.append("Passwords do not match.")
    if email and not valid_email(email):
        errors.append("Enter a valid email address.")
    if not terms:
        errors.append("You must accept the Terms of Service.")
    return errors
