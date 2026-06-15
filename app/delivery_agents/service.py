"""
Delivery Agents Service Module
"""

from app.extensions import db
from app.models.shipment import Shipment
from app.models.tracking import Tracking
from app.models.delivery_proof import DeliveryProof
from app.delivery_agents.utils import (
    validate_proof_text,
    agent_owns_shipment,
    validate_shipment_status,
    is_valid_status_transition,
    get_active_agent,
)
from app.notifications.service import NotificationService


class AgentService:
    """Service class for delivery agent operations."""

    def __init__(self):
        self.notification_service = NotificationService()

    def list_assigned_shipments(self, agent_id, status=None, page=1, per_page=20):
        """Return shipments assigned to a delivery agent."""
        query = Shipment.query.filter_by(agent_id=agent_id)

        if status:
            status = status.strip().upper()
            if not validate_shipment_status(status):
                raise ValueError('Invalid shipment status filter')
            query = query.filter_by(status=status)

        pagination = query.order_by(Shipment.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )

        return {
            'items': [shipment.to_dict(include_history=True) for shipment in pagination.items],
            'meta': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
            },
        }

    def assign_agent_to_shipment(self, shipment_id, agent_id):
        """Assign a delivery agent to a shipment (admin only)."""
        shipment = Shipment.query.filter_by(id=shipment_id).first()
        if not shipment:
            raise ValueError('Shipment not found')

        try:
            agent_id = int(agent_id)
        except (TypeError, ValueError):
            raise ValueError('Agent ID is required')

        agent = get_active_agent(agent_id)
        if not agent:
            raise ValueError('Delivery agent not found')

        shipment.agent_id = agent.id
        db.session.add(shipment)
        self.notification_service.notify_shipment_assigned(shipment, agent.id)
        db.session.commit()

        return shipment.to_dict(include_history=True)

    def update_shipment_status(self, shipment_id, new_status, current_user):
        """Update shipment status with role-based access control."""
        shipment = Shipment.query.filter_by(id=shipment_id).first()
        if not shipment:
            raise ValueError('Shipment not found')

        if current_user.is_agent():
            if not agent_owns_shipment(shipment, current_user.id):
                raise ValueError('Shipment not assigned to you')
        elif not current_user.is_admin():
            raise ValueError('Forbidden')

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
            updated_by=current_user.id,
        )
        self.notification_service.notify_shipment_status_changed(shipment, new_status)
        db.session.commit()

        return shipment.to_dict(include_history=True)

    def submit_delivery_proof(self, shipment_id, proof_text, current_user):
        """Submit delivery proof for an assigned shipment."""
        if not current_user.is_agent():
            raise ValueError('Forbidden')

        shipment = Shipment.query.filter_by(id=shipment_id).first()
        if not shipment:
            raise ValueError('Shipment not found')

        if not agent_owns_shipment(shipment, current_user.id):
            raise ValueError('Shipment not assigned to you')

        if not validate_proof_text(proof_text):
            raise ValueError('Proof text is required')

        proof = DeliveryProof(
            shipment_id=shipment.id,
            proof_text=proof_text.strip(),
        )
        db.session.add(proof)
        db.session.commit()

        return proof.to_dict()

    def _create_tracking_event(self, shipment_id, status, updated_by):
        """Record a tracking history entry."""
        tracking = Tracking(
            shipment_id=shipment_id,
            status=status,
            updated_by=updated_by,
        )
        db.session.add(tracking)
        return tracking
