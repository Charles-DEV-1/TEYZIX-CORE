"""
Notifications Package

PURPOSE:
    Centralize all notification-related functionality.
    Handle notification management and delivery operations.

RESPONSIBILITIES:
    - Import notification components
    - Expose notification blueprint
    - Manage notifications module organization

WHEN TO USE:
    - Register notification blueprint in app factory
    - Import notification service in other modules

WHAT NOT TO PUT HERE:
    - Individual component logic (define in separate files)
    - Route handlers (handle in routes.py)
    - Business logic (handle in service.py)
"""

from .routes import notifications_bp
from .service import NotificationService
from . import utils

__all__ = ['notifications_bp', 'NotificationService', 'utils']
