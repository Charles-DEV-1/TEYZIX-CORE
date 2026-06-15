"""
Authentication Middleware Module

PURPOSE:
    Provide authentication middleware for protecting routes.
    Handle JWT token validation and user verification.
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User


def auth_required(f):
    """Decorator that verifies a JWT and loads the current user."""

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()
            if identity is None:
                raise RuntimeError('Invalid token identity')

            try:
                identity_value = int(identity)
            except (TypeError, ValueError):
                identity_value = identity

            user = User.query.get(identity_value)
            if not user or not user.is_active:
                return jsonify({'success': False, 'message': 'Unauthorized'}), 401

            return f(current_user=user, *args, **kwargs)
        except Exception:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    return decorated
