"""
Configuration Package

PURPOSE:
    Centralize all application configuration.
    Manage environment-specific settings.

RESPONSIBILITIES:
    - Import configuration classes
    - Expose configuration to app factory
    - Support multiple environments

WHEN TO USE:
    - Import from config in app factory
    - Select appropriate config based on environment

WHAT NOT TO PUT HERE:
    - Individual config logic (define in separate files)
    - Business logic
    - Model definitions
"""

from .base import Config
from .development import DevelopmentConfig
from .production import ProductionConfig
from .testing import TestingConfig

__all__ = ['Config', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig']
