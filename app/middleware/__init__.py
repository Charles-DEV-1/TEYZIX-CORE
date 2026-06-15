"""
Middleware Package

PURPOSE:
    Centralize all middleware components for request processing.
    Provide authentication and authorization decorators.

RESPONSIBILITIES:
    - Import middleware components
    - Expose middleware to application
    - Manage middleware initialization

WHEN TO USE:
    - Import middleware decorators in routes
    - Apply to route handlers for protection

WHAT NOT TO PUT HERE:
    - Individual middleware logic (define in separate files)
    - Business logic
    - Route handlers
"""

from .auth_middleware import auth_required
from .role_middleware import require_role

__all__ = ['auth_required', 'require_role']
