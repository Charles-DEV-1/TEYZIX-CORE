"""
Reports Service Module
"""

from datetime import datetime, timedelta

from app.models.shipment import Shipment
from app.models.warehouse import Warehouse


class ReportService:
    """Service class for generating simple JSON reports."""

    def _shipment_summary(self):
        """Return overall shipment counts."""
        total = Shipment.query.count()
        delivered = Shipment.query.filter_by(status=Shipment.STATUS_DELIVERED).count()
        pending = Shipment.query.filter(Shipment.status != Shipment.STATUS_DELIVERED).count()

        return {
            'total_shipments': total,
            'delivered_shipments': delivered,
            'pending_shipments': pending,
        }

    def get_daily_shipments(self):
        """Report shipments created today."""
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow_start = today_start + timedelta(days=1)

        daily_query = Shipment.query.filter(
            Shipment.created_at >= today_start,
            Shipment.created_at < tomorrow_start,
        )

        total_today = daily_query.count()
        delivered_today = daily_query.filter_by(status=Shipment.STATUS_DELIVERED).count()
        pending_today = total_today - delivered_today

        shipments = daily_query.order_by(Shipment.created_at.desc()).all()

        return {
            'date': today_start.date().isoformat(),
            'total_shipments': total_today,
            'delivered_shipments': delivered_today,
            'pending_shipments': pending_today,
            'shipments': [shipment.to_dict() for shipment in shipments],
        }

    def get_delivered_report(self):
        """Report all delivered shipments."""
        summary = self._shipment_summary()
        delivered_query = Shipment.query.filter_by(status=Shipment.STATUS_DELIVERED)
        shipments = delivered_query.order_by(Shipment.updated_at.desc()).all()

        return {
            **summary,
            'shipments': [shipment.to_dict() for shipment in shipments],
        }

    def get_pending_report(self):
        """Report all shipments that are not yet delivered."""
        summary = self._shipment_summary()
        pending_query = Shipment.query.filter(Shipment.status != Shipment.STATUS_DELIVERED)
        shipments = pending_query.order_by(Shipment.created_at.desc()).all()

        return {
            **summary,
            'shipments': [shipment.to_dict() for shipment in shipments],
        }

    def get_warehouse_utilization(self):
        """Report warehouse capacity utilization."""
        summary = self._shipment_summary()
        warehouses = Warehouse.query.order_by(Warehouse.name.asc()).all()

        total_capacity = sum(warehouse.capacity for warehouse in warehouses)
        total_load = sum(warehouse.current_load for warehouse in warehouses)

        if total_capacity > 0:
            overall_utilization = round((total_load / total_capacity) * 100, 2)
        else:
            overall_utilization = 0

        return {
            **summary,
            'overall_utilization_percentage': overall_utilization,
            'warehouses': [
                {
                    'id': warehouse.id,
                    'name': warehouse.name,
                    'location': warehouse.location,
                    'capacity': warehouse.capacity,
                    'current_load': warehouse.current_load,
                    'utilization_percentage': round(warehouse.utilization_percentage, 2),
                }
                for warehouse in warehouses
            ],
        }
