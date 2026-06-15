"""
Configuration Base Module

PURPOSE:
    Provide base configuration class with default settings.
    Define environment variables and their defaults.

RESPONSIBILITIES:
    - Set base configuration values
    - Define database connections
    - Configure JWT settings
    - Set logging levels

WHEN TO USE:
    - Inherit from this class in environment-specific configs
    - Override settings in child classes
    - Import in app factory for base settings

WHAT NOT TO PUT HERE:
    - Business logic
    - Route handlers
    - Sensitive data (use environment variables)
    - Model definitions
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class with default settings"""

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ALGORITHM = 'HS256'
    JWT_ERROR_MESSAGE_KEY = 'message'
    PASSWORD_RESET_TOKEN_EXPIRES = timedelta(hours=1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    REQUIRE_REDIS = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
