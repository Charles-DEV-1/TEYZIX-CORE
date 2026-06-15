"""
Bcrypt Extension Module

PURPOSE:
    Initialize and manage Flask-Bcrypt for password hashing and verification.
    Provides secure password handling across the application.

RESPONSIBILITIES:
    - Create Bcrypt instance
    - Provide password hashing functionality
    - Provide password verification functionality
    - Ensure cryptographic security

WHEN TO USE:
    - Import bcrypt in auth service for password operations
    - Use in user model operations
    - Reference when handling user registration and login

WHAT NOT TO PUT HERE:
    - Authentication logic
    - Route handlers
    - User model definitions
    - Business logic
"""

from flask_bcrypt import Bcrypt

# Initialize Bcrypt instance
bcrypt = Bcrypt()
