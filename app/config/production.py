"""
Production Configuration Module
"""

import os
from .base import Config


class ProductionConfig(Config):
    """Production environment configuration"""

    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/logistics_db'
    )

    REQUIRE_REDIS = True
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING')

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
