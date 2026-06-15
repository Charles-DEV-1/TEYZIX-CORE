"""
Unit tests for authentication utility helpers.
"""

from app.auth.utils import is_valid_email, is_strong_password, validate_role


def test_is_valid_email_accepts_valid_address():
    assert is_valid_email('user@example.com') is True


def test_is_valid_email_rejects_invalid_address():
    assert is_valid_email('not-an-email') is False


def test_is_strong_password_accepts_valid_password():
    assert is_strong_password('SecurePass1!') is True


def test_is_strong_password_rejects_weak_password():
    assert is_strong_password('short') is False


def test_validate_role_accepts_known_roles():
    assert validate_role('customer') is True
    assert validate_role('admin') is True
    assert validate_role('delivery_agent') is True


def test_validate_role_rejects_unknown_role():
    assert validate_role('superuser') is False
