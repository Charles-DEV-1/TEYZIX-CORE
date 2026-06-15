"""
Reports Package

PURPOSE:
    Centralize all reporting and analytics functionality.
    Handle report generation and data analysis operations.

RESPONSIBILITIES:
    - Import report components
    - Expose report blueprint
    - Manage reports module organization

WHEN TO USE:
    - Register report blueprint in app factory
    - Import report service in other modules

WHAT NOT TO PUT HERE:
    - Individual component logic (define in separate files)
    - Route handlers (handle in routes.py)
    - Business logic (handle in service.py)
"""

from .routes import reports_bp
from .service import ReportService

__all__ = ['reports_bp', 'ReportService']
