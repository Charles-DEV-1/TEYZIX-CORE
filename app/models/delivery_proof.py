"""
Delivery Proof Model Module

PURPOSE:
    Define the DeliveryProof model for recording delivery confirmations.
    Store proof of delivery information.

RESPONSIBILITIES:
    - Store delivery proof records
    - Track delivery completion evidence
    - Reference shipments
    - Maintain delivery timestamps

RELATIONSHIPS:
    - Many-to-One: shipment
"""

from datetime import datetime
from app.extensions import db

class DeliveryProof(db.Model):
    """DeliveryProof model for storing delivery confirmation proof."""
    
    __tablename__ = 'delivery_proofs'
    __table_args__ = (
        db.Index('ix_delivery_proofs_shipment_id', 'shipment_id'),
        db.Index('ix_delivery_proofs_created_at', 'created_at'),
    )
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipments.id'), nullable=False, index=True)
    
    # Proof Information
    proof_text = db.Column(db.Text, nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<DeliveryProof {self.id} - Shipment {self.shipment_id}>'
    
    def to_dict(self):
        """Convert delivery proof to dictionary."""
        return {
            'id': self.id,
            'shipment_id': self.shipment_id,
            'proof_text': self.proof_text,
            'created_at': self.created_at.isoformat(),
        }
