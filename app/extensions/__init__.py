"""
Extensions Package

PURPOSE:
    Centralize all Flask extensions initialization.
    Provides a single import point for all initialized extensions.

RESPONSIBILITIES:
    - Import and expose all extensions
    - Ensure extensions are available across the application
    - Manage extension configurations

WHEN TO USE:
    - Import extensions from this module in other parts of the application
    - Initialize extensions in app factory

WHAT NOT TO PUT HERE:
    - Individual extension logic (define in separate files)
    - Business logic
    - Configuration
"""

from .db import db
from .jwt import jwt
from .bcrypt import bcrypt
from .mail import mail
try:
    from .redis import redis_client
except Exception:
    redis_client = None
from flask_migrate import Migrate

migrate = Migrate()

__all__ = ['db', 'jwt', 'bcrypt', 'mail', 'redis_client', 'migrate']
