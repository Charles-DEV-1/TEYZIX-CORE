"""
Tracking Model Module

PURPOSE:
    Define the Tracking model for recording shipment tracking events.
    Record status changes and history for shipment timeline.

RESPONSIBILITIES:
    - Store tracking event information
    - Record status changes with timestamps
    - Track who updated the shipment status
    - Maintain shipment history

RELATIONSHIPS:
    - Many-to-One: shipment
    - Many-to-One: user (updated_by)
"""

from datetime import datetime
from app.extensions import db

class Tracking(db.Model):
    """Tracking model for recording shipment tracking events."""
    
    __tablename__ = 'tracking_history'
    __table_args__ = (
        db.Index('ix_tracking_shipment_id', 'shipment_id'),
        db.Index('ix_tracking_updated_by', 'updated_by'),
        db.Index('ix_tracking_timestamp', 'timestamp'),
    )
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.id'), nullable=False, index=True)
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Status Information
    status = db.Column(db.String(20), nullable=False)
    
    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Tracking {self.id} - {self.shipment_id} to {self.status}>'
    
    def to_dict(self):
        """Convert tracking to dictionary."""
        return {
            'id': self.id,
            'shipment_id': self.shipment_id,
            'status': self.status,
            'updated_by': self.updated_by,
            'timestamp': self.timestamp.isoformat(),
        }
