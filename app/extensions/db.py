"""
Database Extension Module

PURPOSE:
    Initialize and manage SQLAlchemy database connection for the Flask application.
    Provides a centralized database instance that can be imported across the application.

RESPONSIBILITIES:
    - Create SQLAlchemy instance
    - Handle database configuration
    - Provide ORM for model definitions
    - Manage database sessions

WHEN TO USE:
    - Import db when defining models
    - Use in app factory to initialize with Flask app
    - Reference in service layers for database operations

WHAT NOT TO PUT HERE:
    - Business logic
    - Route handlers
    - Model definitions (define in models/ module)
    - Service implementations
    - Configuration logic (handle in config/)
"""

from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()
