"""
Warehouses Package

PURPOSE:
    Centralize all warehouse-related functionality.
    Handle warehouse management and inventory operations.

RESPONSIBILITIES:
    - Import warehouse components
    - Expose warehouse blueprint
    - Manage warehouse module organization

WHEN TO USE:
    - Register warehouse blueprint in app factory
    - Import warehouse service in other modules

WHAT NOT TO PUT HERE:
    - Individual component logic (define in separate files)
    - Route handlers (handle in routes.py)
    - Business logic (handle in service.py)
"""

from .routes import warehouses_bp
from .service import WarehouseService
from . import utils

__all__ = ['warehouses_bp', 'WarehouseService', 'utils']
