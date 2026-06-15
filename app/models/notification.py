"""
Notification Model Module

PURPOSE:
    Define the Notification model for user notifications.
    Handle notification storage and status management.

RESPONSIBILITIES:
    - Store notification records
    - Track notification read status
    - Reference related shipments
    - Support notification queries

RELATIONSHIPS:
    - Many-to-One: user
    - Many-to-One: shipment (optional)
"""

from datetime import datetime
from app.extensions import db

class Notification(db.Model):
    """Notification model for storing user notifications."""
    
    __tablename__ = 'notifications'
    __table_args__ = (
        db.Index('ix_notifications_user_id', 'user_id'),
        db.Index('ix_notifications_is_read', 'is_read'),
        db.Index('ix_notifications_created_at', 'created_at'),
    )
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.id'), nullable=True, index=True)
    
    # Message
    message = db.Column(db.Text, nullable=False)
    
    # Status
    is_read = db.Column(db.Boolean, default=False, nullable=False, index=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Notification {self.id} - User {self.user_id}>'
    
    def mark_as_read(self):
        """Mark notification as read (caller should commit)."""
        self.is_read = True
    
    def to_dict(self):
        """Convert notification to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'shipment_id': self.shipment_id,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
        }
