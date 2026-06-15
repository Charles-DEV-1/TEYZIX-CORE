"""
Models Package

PURPOSE:
    Centralize all SQLAlchemy model definitions.
    Provide ORM representation of database entities.

RESPONSIBILITIES:
    - Import all model classes
    - Expose models to application
    - Manage model organization

WHEN TO USE:
    - Import models for database operations
    - Reference in service layers
    - Query models in route handlers

WHAT NOT TO PUT HERE:
    - Individual model logic (define in separate files)
    - Business logic
    - Route handlers
    - Service implementations
"""

from .user import User
from .shipment import Shipment
from .warehouse import Warehouse
from .tracking import Tracking
from .notification import Notification
from .refresh_token import RefreshToken
from .password_reset_token import PasswordResetToken
from .delivery_proof import DeliveryProof

__all__ = [
    'User',
    'Shipment',
    'Warehouse',
    'Tracking',
    'Notification',
    'RefreshToken',
    'PasswordResetToken',
    'DeliveryProof',
]
