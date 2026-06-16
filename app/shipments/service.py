"""
Shipments Service Module

PURPOSE:
    Implement shipment business logic.
    Handle shipment operations, tracking, and status management.

RESPONSIBILITIES:
    - Shipment creation and validation
    - Shipment status management
    - Tracking event recording
    - Shipment queries and filtering

WHEN TO USE:
    - Call from route handlers
    - Handle all shipment-related operations
    - Manage shipment lifecycle

WHAT NOT TO PUT HERE:
    - Route handlers (handle in routes.py)
    - Request/response handling (handle in routes.py)
    - Validation schemas (use marshmallow separately)
    - Middleware logic (handle in middleware/)
"""

from app.extensions import db
from app.models.shipment import Shipment
from app.models.tracking import Tracking
from app.models.warehouse import Warehouse
from app.shipments.utils import (
    generate_shipment_id,
    validate_shipment_status,
    is_valid_status_transition,
)
from app.warehouses.utils import can_accept_load
from app.models.user import User
from app.notifications.service import NotificationService
from app.notifications.email_service import send_shipment_created_email


class ShipmentService:
    """Service class for handling shipment operations."""

    def __init__(self):
        self.Shipment = Shipment
        self.Tracking = Tracking
        self.notification_service = NotificationService()

    def create_shipment(
        self,
        sender_name,
        sender_phone,
        receiver_name,
        receiver_phone,
        package_type,
        weight,
        delivery_address,
        customer_id,
        warehouse_id=None,
        assigned_agent_id=None,
    ):
        """Create a new shipment and record initial tracking history."""
        sender_name = (sender_name or '').strip()
        sender_phone = (sender_phone or '').strip()
        receiver_name = (receiver_name or '').strip()
        receiver_phone = (receiver_phone or '').strip()
        package_type = (package_type or '').strip()
        delivery_address = (delivery_address or '').strip()

        if not sender_name:
            raise ValueError('Sender name is required')
        if not sender_phone:
            raise ValueError('Sender phone is required')
        if not receiver_name:
            raise ValueError('Receiver name is required')
        if not receiver_phone:
            raise ValueError('Receiver phone is required')
        if not package_type:
            raise ValueError('Package type is required')
        try:
            weight = float(weight)
        except (TypeError, ValueError):
            raise ValueError('Weight must be a number')

        if weight <= 0:
            raise ValueError('Weight must be greater than zero')
        if not delivery_address:
            raise ValueError('Delivery address is required')
        if not customer_id:
            raise ValueError('Customer information is required')

        warehouse = None
        if warehouse_id:
            warehouse = Warehouse.query.filter_by(id=warehouse_id).first()
            if not warehouse:
                raise ValueError('Warehouse not found')
            if not can_accept_load(warehouse.capacity, warehouse.current_load, weight):
                raise ValueError('Warehouse does not have enough available capacity')

        tracking_id = generate_shipment_id()
        shipment = self.Shipment(
            tracking_id=tracking_id,
            sender_name=sender_name,
            sender_phone=sender_phone,
            receiver_name=receiver_name,
            receiver_phone=receiver_phone,
            package_type=package_type,
            weight=weight,
            delivery_address=delivery_address,
            customer_id=customer_id,
            warehouse_id=warehouse_id,
            agent_id=assigned_agent_id,
        )

        if warehouse:
            warehouse.current_load += weight
            db.session.add(warehouse)

        db.session.add(shipment)
        db.session.flush()
        self._create_tracking_event(
            shipment_id=shipment.id,
            status=shipment.status,
            updated_by=customer_id,
        )
        self.notification_service.notify_shipment_created(shipment)
        if assigned_agent_id:
            self.notification_service.notify_shipment_assigned(shipment, assigned_agent_id)
        db.session.commit()

        customer = User.query.get(customer_id)
        if customer:
            send_shipment_created_email(customer, shipment)

        return shipment.to_dict(include_history=True)

    def get_shipment(self, shipment_id):
        """Retrieve a shipment by its database ID."""
        shipment = self.Shipment.query.filter_by(id=shipment_id).first()
        if not shipment:
            raise ValueError('Shipment not found')

        return shipment.to_dict(include_history=True)

    def list_shipments(self, status=None, tracking_id=None, page=1, per_page=20, customer_id=None):
        """List shipments with optional filters and pagination."""
        query = self.Shipment.query

        if status:
            if not validate_shipment_status(status):
                raise ValueError('Invalid shipment status filter')
            query = query.filter_by(status=status)

        if tracking_id:
            query = query.filter(self.Shipment.tracking_id.ilike(f'%{tracking_id.strip()}%'))

        if customer_id:
            query = query.filter_by(customer_id=customer_id)

        pagination = query.order_by(self.Shipment.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )

        return {
            'items': [shipment.to_dict() for shipment in pagination.items],
            'meta': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
            },
        }

    def search_shipments(self, tracking_id, status=None, page=1, per_page=20):
        """Search shipments by tracking ID and optionally filter by status."""
        if not tracking_id:
            raise ValueError('Tracking ID is required for search')
        return self.list_shipments(status=status, tracking_id=tracking_id, page=page, per_page=per_page)

    def track_shipment(self, tracking_id):
        """Return shipment details for a tracking identifier."""
        shipment = self.Shipment.query.filter_by(tracking_id=tracking_id).first()
        if not shipment:
            raise ValueError('Shipment not found')

        return shipment.to_dict(include_history=True)

    def update_shipment_status(self, shipment_id, new_status, updated_by):
        """Update the current shipment status and record tracking history."""
        shipment = self.Shipment.query.filter_by(id=shipment_id).first()
        if not shipment:
            raise ValueError('Shipment not found')

        new_status = (new_status or '').strip().upper()
        if not validate_shipment_status(new_status):
            raise ValueError('Invalid shipment status')

        if shipment.status == new_status:
            raise ValueError('Shipment already has this status')

        if not is_valid_status_transition(shipment.status, new_status):
            raise ValueError(f'Cannot move status from {shipment.status} to {new_status}')

        shipment.status = new_status
        db.session.add(shipment)
        self._create_tracking_event(
            shipment_id=shipment.id,
            status=new_status,
            updated_by=updated_by,
        )
        db.session.commit()

        return shipment.to_dict(include_history=True)

    def get_tracking_history(self, shipment_id):
        """Return the tracking history for a shipment."""
        history = (
            self.Tracking.query
            .filter_by(shipment_id=shipment_id)
            .order_by(self.Tracking.timestamp.asc())
            .all()
        )
        return [event.to_dict() for event in history]

    def _create_tracking_event(self, shipment_id, status, updated_by):
        """Add a single tracking history record."""
        if not shipment_id or not updated_by:
            raise ValueError('Tracking event requires shipment and user IDs')

        tracking = self.Tracking(
            shipment_id=shipment_id,
            status=status,
            updated_by=updated_by,
        )
        db.session.add(tracking)
        return tracking
