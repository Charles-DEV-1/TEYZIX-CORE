"""
Warehouse Model Module

PURPOSE:
    Define the Warehouse model representing physical warehouse locations.
    Handle warehouse capacity and inventory management.

RESPONSIBILITIES:
    - Store warehouse location information
    - Track warehouse capacity and current load
    - Manage warehouse inventory status

RELATIONSHIPS:
    - One-to-Many: shipments
"""

from datetime import datetime
from app.extensions import db

class Warehouse(db.Model):
    """Warehouse model for representing physical warehouse locations."""
    
    __tablename__ = 'warehouses'
    __table_args__ = (
        db.Index('ix_warehouses_name', 'name'),
        db.Index('ix_warehouses_location', 'location'),
    )
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Warehouse Information
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    location = db.Column(db.String(255), nullable=False, index=True)
    
    # Capacity Management
    capacity = db.Column(db.Float, nullable=False)  # Total capacity
    current_load = db.Column(db.Float, default=0, nullable=False)  # Current load
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    shipments = db.relationship(
        'Shipment',
        backref='warehouse',
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<Warehouse {self.id} - {self.name}>'
    
    def __str__(self):
        return self.name
    
    @property
    def available_capacity(self):
        """Get remaining available capacity."""
        return self.capacity - self.current_load
    
    @property
    def utilization_percentage(self):
        """Get capacity utilization percentage."""
        if self.capacity == 0:
            return 0
        return (self.current_load / self.capacity) * 100
    
    def is_full(self):
        """Check if warehouse is at capacity."""
        return self.current_load >= self.capacity
    
    def can_accommodate(self, weight):
        """Check if warehouse can accommodate additional weight."""
        return (self.current_load + weight) <= self.capacity
    
    def to_dict(self):
        """Convert warehouse to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'capacity': self.capacity,
            'current_load': self.current_load,
            'available_capacity': self.available_capacity,
            'utilization_percentage': self.utilization_percentage,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
