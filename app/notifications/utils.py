"""
Notifications Utilities Module
"""

# Event types used when creating shipment-related notifications
EVENT_SHIPMENT_CREATED = 'shipment_created'
EVENT_SHIPMENT_ASSIGNED = 'shipment_assigned'
EVENT_SHIPMENT_STATUS_CHANGED = 'shipment_status_changed'
EVENT_SHIPMENT_DELIVERED = 'shipment_delivered'


def build_shipment_created_message(tracking_id):
    """Message when a new shipment is created."""
    return f'Your shipment {tracking_id} has been created successfully.'


def build_shipment_assigned_message(tracking_id, for_agent=False):
    """Message when a delivery agent is assigned to a shipment."""
    if for_agent:
        return f'You have been assigned to deliver shipment {tracking_id}.'
    return f'A delivery agent has been assigned to your shipment {tracking_id}.'


def build_status_changed_message(tracking_id, new_status):
    """Message when a shipment status is updated."""
    return f'Shipment {tracking_id} status has been updated to {new_status}.'


def build_delivered_message(tracking_id):
    """Message when a shipment is delivered."""
    return f'Your shipment {tracking_id} has been delivered.'
