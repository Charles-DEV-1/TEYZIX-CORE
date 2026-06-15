"""
Password Reset Token Model Module

PURPOSE:
    Define the PasswordResetToken model for password reset functionality.
    Handle password reset token storage and validation.

RESPONSIBILITIES:
    - Store password reset tokens
    - Track token expiration
    - Mark tokens as used
    - Support password reset workflow

RELATIONSHIPS:
    - Many-to-One: user
"""

from datetime import datetime
from app.extensions import db

class PasswordResetToken(db.Model):
    """PasswordResetToken model for managing password reset tokens."""
    
    __tablename__ = 'password_reset_tokens'
    __table_args__ = (
        db.Index('ix_password_reset_tokens_user_id', 'user_id'),
        db.Index('ix_password_reset_tokens_token', 'token'),
    )
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Token Information
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    
    # Token Status
    used = db.Column(db.Boolean, default=False, nullable=False)
    
    # Token Expiration
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<PasswordResetToken {self.id} - User {self.user_id}>'
    
    def is_expired(self):
        """Check if token is expired."""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Check if token is valid (not expired and not used)."""
        return not self.is_expired() and not self.used
    
    def mark_as_used(self):
        """Mark token as used."""
        self.used = True
        db.session.commit()
    
    def to_dict(self):
        """Convert token to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'used': self.used,
            'expires_at': self.expires_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'is_valid': self.is_valid(),
        }
