"""
User Model Module

PURPOSE:
    Define the User model representing application users/employees.
    Handle user attributes and relationships with other entities.

RESPONSIBILITIES:
    - Store user authentication data (email, password hash)
    - Manage user roles and permissions
    - Track user active status
    - Maintain user creation/update timestamps

RELATIONSHIPS:
    - One-to-Many: shipments (as customer)
    - One-to-Many: shipments (as agent)
    - One-to-Many: tracking_history (as updated_by)
    - One-to-Many: refresh_tokens
    - One-to-Many: password_reset_tokens
    - One-to-Many: notifications
    - Many-to-One: warehouse (if assigned)
"""

from datetime import datetime
from app.extensions import db

class User(db.Model):
    """User model for authentication and authorization."""
    
    __tablename__ = 'users'
    __table_args__ = (
        db.Index('ix_users_email', 'email'),
        db.Index('ix_users_role', 'role'),
    )
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User Information
    name = db.Column(db.String(120), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # User Role (customer, delivery_agent, admin)
    ROLE_CUSTOMER = 'customer'
    ROLE_AGENT = 'delivery_agent'
    ROLE_ADMIN = 'admin'
    
    role = db.Column(
        db.String(20),
        default=ROLE_CUSTOMER,
        nullable=False,
        index=True
    )
    
    # Account Status
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    
    # Relationships
    # Shipments where user is customer
    shipments_as_customer = db.relationship(
        'Shipment',
        foreign_keys='Shipment.customer_id',
        backref='customer',
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    # Shipments where user is agent
    shipments_as_agent = db.relationship(
        'Shipment',
        foreign_keys='Shipment.agent_id',
        backref='agent',
        lazy='select'
    )
    
    # Tracking history updates
    tracking_updates = db.relationship(
        'Tracking',
        foreign_keys='Tracking.updated_by',
        backref='updated_by_user',
        lazy='select'
    )
    
    # Refresh tokens
    refresh_tokens = db.relationship(
        'RefreshToken',
        backref='user',
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    # Password reset tokens
    password_reset_tokens = db.relationship(
        'PasswordResetToken',
        backref='user',
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    # Notifications
    notifications = db.relationship(
        'Notification',
        backref='user',
        lazy='select',
        cascade='all, delete-orphan'
    )
    
    def __repr__(self):
        return f'<User {self.id} - {self.email} ({self.role})>'
    
    def __str__(self):
        return self.email
    
    def is_admin(self):
        """Check if user is admin."""
        return self.role == self.ROLE_ADMIN
    
    def is_agent(self):
        """Check if user is delivery agent."""
        return self.role == self.ROLE_AGENT
    
    def is_customer(self):
        """Check if user is customer."""
        return self.role == self.ROLE_CUSTOMER
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary."""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_sensitive:
            data['password_hash'] = self.password_hash
        return data
