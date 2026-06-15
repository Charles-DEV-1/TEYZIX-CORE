"""
Authentication Package

PURPOSE:
    Centralize all authentication-related functionality.
    Handle user authentication, authorization, and token management.

RESPONSIBILITIES:
    - Import auth components
    - Expose auth blueprint
    - Manage auth module organization

WHEN TO USE:
    - Register auth blueprint in app factory
    - Import auth service in other modules

WHAT NOT TO PUT HERE:
    - Individual component logic (define in separate files)
    - Route handlers (handle in routes.py)
    - Business logic (handle in service.py)
"""

from .routes import auth_bp
from .service import AuthService
from . import utils

__all__ = ['auth_bp', 'AuthService', 'utils']
