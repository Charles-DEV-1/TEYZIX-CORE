"""
Warehouse utility helpers.
"""


def normalize_name(value):
    """Return a trimmed warehouse name."""
    return (value or '').strip()


def normalize_location(value):
    """Return a trimmed warehouse location."""
    return (value or '').strip()


def parse_positive_float(value, field_name):
    """Parse and validate a positive float field."""
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        raise ValueError(f'{field_name} must be a number')

    if parsed <= 0:
        raise ValueError(f'{field_name} must be greater than zero')

    return parsed


def calculate_available_capacity(capacity, current_load):
    """Calculate remaining warehouse capacity."""
    return capacity - current_load


def can_accept_load(capacity, current_load, additional_load):
    """Check whether a warehouse can accept more load."""
    return current_load + additional_load <= capacity
