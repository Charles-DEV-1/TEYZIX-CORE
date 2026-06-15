"""
Development Configuration Module

PURPOSE:
    Provide development environment specific configuration.
    Override base settings suitable for local development.

RESPONSIBILITIES:
    - Set development environment variables
    - Enable debug mode
    - Configure development database
    - Set development logging levels

WHEN TO USE:
    - Use in app factory when FLASK_ENV is 'development'
    - Set DEBUG=True for auto-reloading
    - Use development database credentials

WHAT NOT TO PUT HERE:
    - Business logic
    - Route handlers
    - Sensitive production data
    - Model definitions
"""

import os
from .base import Config

class DevelopmentConfig(Config):
    """Development environment configuration"""

    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/logistics_dev'
    )

    REQUIRE_REDIS = False
    LOG_LEVEL = 'DEBUG'
