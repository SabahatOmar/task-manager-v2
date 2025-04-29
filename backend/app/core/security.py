# core/security.py

from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hashes a password"""
    return generate_password_hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    """Verifies a password"""
    return check_password_hash(hashed_password, password)
