"""
JWT Extension Module

PURPOSE:
    Initialize and manage Flask-JWT-Extended for token-based authentication.
    Provides JWT token creation and validation across the application.

RESPONSIBILITIES:
    - Create JWT manager instance
    - Handle JWT configuration
    - Provide decorators for route protection
    - Manage token validation

WHEN TO USE:
    - Import jwt when protecting routes
    - Use in auth service for token generation
    - Reference in middleware for token verification

WHAT NOT TO PUT HERE:
    - Authentication logic (handle in auth/service.py)
    - Route handlers (handle in routes.py)
    - Business logic
    - Token storage logic
"""

from flask_jwt_extended import JWTManager

# Initialize JWT Manager instance
jwt = JWTManager()
