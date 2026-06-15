"""
Shipments Utilities Module

PURPOSE:
    Provide helper functions for shipment operations.
    Reusable utility functions for shipment management.

RESPONSIBILITIES:
    - Shipment ID generation
    - Status validation
    - Distance calculations
    - Delivery time estimation

WHEN TO USE:
    - Import in service.py for utility functions
    - Use for common shipment operations
    - Reuse across shipment code

WHAT NOT TO PUT HERE:
    - Business logic (handle in service.py)
    - Route handlers (handle in routes.py)
    - Database operations (handle in service.py)

TODO - Utility functions to implement:
    - generate_shipment_id()
      Generate unique shipment ID
    
    - validate_shipment_status(status)
      Validate shipment status is valid
      Valid statuses: pending, in_transit, delivered, cancelled, failed
    
    - is_valid_status_transition(current_status, new_status)
      Check if status transition is allowed
    
    - calculate_delivery_distance(origin_coords, destination_coords)
      Calculate distance between two points
    
    - estimate_delivery_time(distance, weather_factor)
      Estimate delivery time based on distance
    
    - calculate_shipping_cost(weight, distance, service_type)
      Calculate shipping cost based on parameters
"""

from datetime import datetime
import secrets
import string

from app.models.shipment import Shipment


def generate_shipment_id():
    """Generate a short unique tracking ID for a shipment."""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    suffix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f'SHP{timestamp}{suffix}'


def validate_shipment_status(status):
    """Validate a shipment status against the allowed values."""
    if not status or not isinstance(status, str):
        return False
    return status.upper() in Shipment.VALID_STATUSES


def is_valid_status_transition(current_status, new_status):
    """Check whether the shipment can move from one status to another."""
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


def calculate_delivery_distance(origin_coords, destination_coords):
    """Estimate delivery distance. Placeholder for future distance logic."""
    return None


def estimate_delivery_time(distance, weather_factor=1.0):
    """Estimate delivery time. Placeholder for future delivery timing logic."""
    return None


def calculate_shipping_cost(weight, distance, service_type='standard'):
    """Calculate shipping cost. Placeholder for future cost estimation."""
    return None

