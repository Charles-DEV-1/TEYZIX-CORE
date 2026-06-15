"""
Delivery Agents Utilities Module
"""

from app.models.shipment import Shipment
from app.models.user import User


def validate_proof_text(proof_text):
    """Validate delivery proof text is present."""
    if not proof_text or not isinstance(proof_text, str):
        return False
    return bool(proof_text.strip())


def is_delivery_agent(user):
    """Check whether a user is an active delivery agent."""
    return user is not None and user.is_active and user.is_agent()


def agent_owns_shipment(shipment, agent_id):
    """Check whether a shipment is assigned to the given agent."""
    return shipment is not None and shipment.agent_id == agent_id


def validate_shipment_status(status):
    """Validate a shipment status value."""
    if not status or not isinstance(status, str):
        return False
    return status.upper() in Shipment.VALID_STATUSES


def is_valid_status_transition(current_status, new_status):
    """Check whether a shipment status transition is allowed."""
    if not validate_shipment_status(current_status) or not validate_shipment_status(new_status):
        return False

    transitions = {
        Shipment.STATUS_CREATED: [Shipment.STATUS_PICKED_UP],
        Shipment.STATUS_PICKED_UP: [Shipment.STATUS_IN_WAREHOUSE],
        Shipment.STATUS_IN_WAREHOUSE: [Shipment.STATUS_OUT_FOR_DELIVERY],
        Shipment.STATUS_OUT_FOR_DELIVERY: [Shipment.STATUS_DELIVERED],
        Shipment.STATUS_DELIVERED: [],
    }
    return new_status.upper() in transitions.get(current_status.upper(), [])


def get_active_agent(agent_id):
    """Fetch an active delivery agent by ID."""
    agent = User.query.filter_by(id=agent_id, role=User.ROLE_AGENT, is_active=True).first()
    return agent
