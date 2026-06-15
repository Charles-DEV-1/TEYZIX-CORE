"""
Shipment Model Module

PURPOSE:
    Define the Shipment model representing logistics shipments.
    Handle shipment tracking and status management.

RESPONSIBILITIES:
    - Store shipment information (sender, receiver, package)
    - Manage shipment status lifecycle
    - Track shipment assignments (warehouse, agent)
    - Maintain shipment metadata

RELATIONSHIPS:
    - Many-to-One: customer (User)
    - Many-to-One: agent (User)
    - Many-to-One: warehouse
    - One-to-Many: tracking_history
    - One-to-Many: delivery_proofs
    - One-to-Many: notifications
"""

from datetime import datetime
from app.extensions import db

class Shipment(db.Model):
    """Shipment model for representing logistics shipments."""
    
    __tablename__ = 'shipments'
    __table_args__ = (
        db.Index('ix_shipments_tracking_id', 'tracking_id'),
        db.Index('ix_shipments_customer_id', 'customer_id'),
        db.Index('ix_shipments_agent_id', 'agent_id'),
        db.Index('ix_shipments_warehouse_id', 'warehouse_id'),
        db.Index('ix_shipments_status', 'status'),
    )
    
    # Status Constants
    STATUS_CREATED = 'CREATED'
    STATUS_PICKED_UP = 'PICKED_UP'
    STATUS_IN_WAREHOUSE = 'IN_WAREHOUSE'
    STATUS_OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY'
    STATUS_DELIVERED = 'DELIVERED'
    
    VALID_STATUSES = [
        STATUS_CREATED,
        STATUS_PICKED_UP,
        STATUS_IN_WAREHOUSE,
        STATUS_OUT_FOR_DELIVERY,
        STATUS_DELIVERED,
    ]
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Tracking Information
    tracking_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Sender Information
    sender_name = db.Column(db.String(120), nullable=False)
    sender_phone = db.Column(db.String(20), nullable=False)
    
    # Receiver Information
    receiver_name = db.Column(db.String(120), nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    
    # Package Information
    package_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)  # in kg
    
    # Delivery Information
    delivery_address = db.Column(db.String(255), nullable=False)
    
    # Status
    status = db.Column(
        db.String(20),
        default=STATUS_CREATED,
        nullable=False,
        index=True
    )
    
    # Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=True, index=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    tracking_history = db.relationship(
        'Tracking',
        backref='shipment',
        lazy='select',
        cascade='all, delete-orphan',
        foreign_keys='Tracking.shipment_id'
    )
    
    delivery_proofs = db.relationship(
        'DeliveryProof',
        backref='shipment',
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    notifications = db.relationship(
        'Notification',
        backref='shipment',
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Shipment {self.id} - {self.tracking_id}>'
    
    def __str__(self):
        return self.tracking_id
    
    @property
    def assigned_agent_id(self):
        """Expose assigned agent id with the expected field name."""
        return self.agent_id
    
    def is_delivered(self):
        """Check if shipment is delivered."""
        return self.status == self.STATUS_DELIVERED
    
    def can_transition_to(self, new_status):
        """Check if status transition is allowed."""
        if new_status not in self.VALID_STATUSES:
            return False
        
        # Define valid transitions
        transitions = {
            self.STATUS_CREATED: [self.STATUS_PICKED_UP],
            self.STATUS_PICKED_UP: [self.STATUS_IN_WAREHOUSE],
            self.STATUS_IN_WAREHOUSE: [self.STATUS_OUT_FOR_DELIVERY],
            self.STATUS_OUT_FOR_DELIVERY: [self.STATUS_DELIVERED],
            self.STATUS_DELIVERED: [],
        }
        
        return new_status in transitions.get(self.status, [])
    
    def to_dict(self, include_history=False):
        """Convert shipment to dictionary."""
        data = {
            'id': self.id,
            'tracking_id': self.tracking_id,
            'sender_name': self.sender_name,
            'sender_phone': self.sender_phone,
            'receiver_name': self.receiver_name,
            'receiver_phone': self.receiver_phone,
            'package_type': self.package_type,
            'weight': self.weight,
            'delivery_address': self.delivery_address,
            'status': self.status,
            'customer_id': self.customer_id,
            'warehouse_id': self.warehouse_id,
            'agent_id': self.agent_id,
            'assigned_agent_id': self.agent_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        
        if include_history:
            data['tracking_history'] = [
                t.to_dict() for t in self.tracking_history
            ]
        
        return data
