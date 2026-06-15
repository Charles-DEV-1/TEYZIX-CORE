"""
Refresh Token Model Module

PURPOSE:
    Define the RefreshToken model for managing JWT refresh tokens.
    Handle token storage, revocation, and expiration.

RESPONSIBILITIES:
    - Store refresh tokens with JTI (JWT ID)
    - Track token expiration
    - Support token revocation
    - Enable token rotation

RELATIONSHIPS:
    - Many-to-One: user
"""

from datetime import datetime
from app.extensions import db

class RefreshToken(db.Model):
    """RefreshToken model for managing JWT refresh tokens."""
    
    __tablename__ = 'refresh_tokens'
    __table_args__ = (
        db.Index('ix_refresh_tokens_user_id', 'user_id'),
        db.Index('ix_refresh_tokens_token_jti', 'token_jti'),
    )
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Token Information
    token_jti = db.Column(db.String(255), unique=True, nullable=False, index=True)
    
    # Token Expiration
    expires_at = db.Column(db.DateTime, nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<RefreshToken {self.id} - User {self.user_id}>'
    
    def is_expired(self):
        """Check if token is expired."""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        """Convert token to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token_jti': self.token_jti,
            'expires_at': self.expires_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'is_expired': self.is_expired(),
        }
