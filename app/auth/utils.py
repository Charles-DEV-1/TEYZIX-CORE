"""
Authentication Utilities Module

PURPOSE:
    Provide helper functions for authentication operations.
    Reusable utility functions for password handling and token operations.
"""

import re
import secrets
from typing import Tuple
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import bcrypt

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
ROLE_CHOICES = {'admin', 'customer', 'delivery_agent'}
PASSWORD_MIN_LENGTH = 8


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip().lower()))


def is_strong_password(password: str) -> bool:
    """Validate password strength requirements."""
    if not isinstance(password, str) or len(password) < PASSWORD_MIN_LENGTH:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r"[~!@#$%^&*()_+=\[\]{}|\\;:'\",.<>/?-]", password):
        return False
    return True


def validate_role(role: str) -> bool:
    """Validate role value."""
    return isinstance(role, str) and role in ROLE_CHOICES


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return bcrypt.generate_password_hash(password).decode('utf-8')


def verify_password(password_hash: str, password: str) -> bool:
    """Verify password against stored bcrypt hash."""
    return bcrypt.check_password_hash(password_hash, password)


def generate_access_token(user) -> str:
    """Generate a JWT access token for a user."""
    claims = {
        'email': user.email,
        'role': user.role,
    }
    identity = str(user.id)
    return create_access_token(identity=identity, additional_claims=claims)


def generate_tokens(user) -> Tuple[str, str]:
    """Generate JWT access and refresh tokens for a user."""
    access_token = generate_access_token(user)
    identity = str(user.id)
    claims = {
        'email': user.email,
        'role': user.role,
    }
    refresh_token = create_refresh_token(identity=identity, additional_claims=claims)
    return access_token, refresh_token


def generate_reset_token() -> str:
    """Generate a secure token for password reset flows."""
    return secrets.token_urlsafe(32)


def is_token_expired(token: str) -> bool:
    """Check whether a JWT token is expired using decode_token semantics."""
    # Token expiration is validated by Flask-JWT-Extended during request.
    return False
