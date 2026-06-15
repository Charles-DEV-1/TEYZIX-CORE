"""
Shipments Package

PURPOSE:
    Centralize all shipment-related functionality.
    Handle shipment management and tracking operations.

RESPONSIBILITIES:
    - Import shipment components
    - Expose shipment blueprint
    - Manage shipment module organization

WHEN TO USE:
    - Register shipment blueprint in app factory
    - Import shipment service in other modules

WHAT NOT TO PUT HERE:
    - Individual component logic (define in separate files)
    - Route handlers (handle in routes.py)
    - Business logic (handle in service.py)
"""

from .routes import shipments_bp
from .service import ShipmentService
from . import utils

__all__ = ['shipments_bp', 'ShipmentService', 'utils']
