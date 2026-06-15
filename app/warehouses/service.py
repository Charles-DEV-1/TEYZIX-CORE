"""
Warehouse business logic.
"""

from app.extensions import db
from app.models.shipment import Shipment
from app.models.warehouse import Warehouse
from app.warehouses.utils import (
    can_accept_load,
    normalize_location,
    normalize_name,
    parse_positive_float,
)


class WarehouseService:
    """Service class for handling warehouse operations."""

    def __init__(self):
        self.Warehouse = Warehouse
        self.Shipment = Shipment

    def create_warehouse(self, name, location, capacity):
        """Create a new warehouse."""
        name = normalize_name(name)
        location = normalize_location(location)
        capacity = parse_positive_float(capacity, 'Capacity')

        if not name:
            raise ValueError('Warehouse name is required')
        if not location:
            raise ValueError('Warehouse location is required')
        if self.Warehouse.query.filter_by(name=name).first():
            raise ValueError('Warehouse name already exists')

        warehouse = self.Warehouse(
            name=name,
            location=location,
            capacity=capacity,
            current_load=0,
        )
        db.session.add(warehouse)
        db.session.commit()

        return warehouse.to_dict()

    def get_warehouse(self, warehouse_id):
        """Get warehouse details."""
        warehouse = self._get_warehouse_or_raise(warehouse_id)
        data = warehouse.to_dict()
        data['shipments'] = [shipment.to_dict() for shipment in warehouse.shipments]
        return data

    def list_warehouses(self, page=1, per_page=20):
        """List warehouses with pagination."""
        pagination = (
            self.Warehouse.query
            .order_by(self.Warehouse.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        return {
            'items': [warehouse.to_dict() for warehouse in pagination.items],
            'meta': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
            },
        }

    def update_warehouse(self, warehouse_id, **updated_fields):
        """Update warehouse information."""
        warehouse = self._get_warehouse_or_raise(warehouse_id)

        if 'name' in updated_fields:
            name = normalize_name(updated_fields.get('name'))
            if not name:
                raise ValueError('Warehouse name is required')
            existing = self.Warehouse.query.filter_by(name=name).first()
            if existing and existing.id != warehouse.id:
                raise ValueError('Warehouse name already exists')
            warehouse.name = name

        if 'location' in updated_fields:
            location = normalize_location(updated_fields.get('location'))
            if not location:
                raise ValueError('Warehouse location is required')
            warehouse.location = location

        if 'capacity' in updated_fields:
            capacity = parse_positive_float(updated_fields.get('capacity'), 'Capacity')
            if capacity < warehouse.current_load:
                raise ValueError('Capacity cannot be less than current load')
            warehouse.capacity = capacity

        db.session.add(warehouse)
        db.session.commit()

        return warehouse.to_dict()

    def delete_warehouse(self, warehouse_id):
        """Delete an empty warehouse."""
        warehouse = self._get_warehouse_or_raise(warehouse_id)
        if warehouse.current_load > 0 or warehouse.shipments:
            raise ValueError('Cannot delete a warehouse with assigned shipments')

        db.session.delete(warehouse)
        db.session.commit()

        return {'id': warehouse_id}

    def assign_shipment_to_warehouse(self, shipment_id, warehouse_id):
        """Assign a shipment to a warehouse and update warehouse loads."""
        if not warehouse_id:
            raise ValueError('Warehouse is required')

        shipment = self.Shipment.query.filter_by(id=shipment_id).first()
        if not shipment:
            raise ValueError('Shipment not found')

        warehouse = self._get_warehouse_or_raise(warehouse_id)
        shipment_weight = float(shipment.weight or 0)

        if shipment.warehouse_id == warehouse.id:
            return shipment.to_dict()

        current_warehouse = shipment.warehouse
        effective_load = warehouse.current_load
        if current_warehouse and current_warehouse.id == warehouse.id:
            effective_load -= shipment_weight

        if not can_accept_load(warehouse.capacity, effective_load, shipment_weight):
            raise ValueError('Warehouse does not have enough available capacity')

        if current_warehouse:
            current_warehouse.current_load = max(
                0,
                current_warehouse.current_load - shipment_weight,
            )
            db.session.add(current_warehouse)

        warehouse.current_load += shipment_weight
        shipment.warehouse_id = warehouse.id

        db.session.add(warehouse)
        db.session.add(shipment)
        db.session.commit()

        return shipment.to_dict()

    def get_warehouse_shipments(self, warehouse_id):
        """Get shipments assigned to a warehouse."""
        warehouse = self._get_warehouse_or_raise(warehouse_id)
        return [shipment.to_dict() for shipment in warehouse.shipments]

    def _get_warehouse_or_raise(self, warehouse_id):
        warehouse = self.Warehouse.query.filter_by(id=warehouse_id).first()
        if not warehouse:
            raise ValueError('Warehouse not found')
        return warehouse
