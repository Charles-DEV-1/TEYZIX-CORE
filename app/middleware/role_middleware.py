"""
Role-Based Authorization Middleware Module

PURPOSE:
    Provide role-based access control (RBAC) middleware.
    Control access to routes based on user roles and permissions.
"""

from functools import wraps
from flask import jsonify


def require_role(*roles):
    """Decorator that ensures the authenticated user has one of the required roles."""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user or current_user.role not in roles:
                return jsonify({'success': False, 'message': 'Forbidden'}), 403
            return f(*args, **kwargs)

        return decorated

    return decorator
