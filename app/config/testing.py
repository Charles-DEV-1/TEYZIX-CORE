"""
Testing configuration for pytest.
"""

from .base import Config


class TestingConfig(Config):
    """In-memory SQLite configuration for automated tests."""

    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    REQUIRE_REDIS = False
