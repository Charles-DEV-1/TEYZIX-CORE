"""
Notifications Service Module
"""

from app.extensions import db
from app.models.notification import Notification
from app.models.shipment import Shipment
from app.notifications.utils import (
    build_shipment_created_message,
    build_shipment_assigned_message,
    build_status_changed_message,
    build_delivered_message,
)


class NotificationService:
    """Service class for database-backed notifications."""

    def create_notification(self, user_id, message, shipment_id=None):
        """Save a new notification for a user."""
        if not user_id:
            raise ValueError('User ID is required')
        if not message or not str(message).strip():
            raise ValueError('Message is required')

        notification = Notification(
            user_id=user_id,
            message=str(message).strip(),
            shipment_id=shipment_id,
            is_read=False,
        )
        db.session.add(notification)
        return notification

    def get_user_notifications(self, user_id, is_read=None, page=1, per_page=20):
        """Return paginated notifications for the current user."""
        query = Notification.query.filter_by(user_id=user_id)

        if is_read is not None:
            query = query.filter_by(is_read=is_read)

        pagination = query.order_by(Notification.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False,
        )

        return {
            'items': [notification.to_dict() for notification in pagination.items],
            'meta': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'pages': pagination.pages,
            },
        }

    def mark_as_read(self, notification_id, user_id):
        """Mark a single notification as read for the owning user."""
        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id,
        ).first()

        if not notification:
            raise ValueError('Notification not found')

        notification.is_read = True
        db.session.add(notification)
        db.session.commit()

        return notification.to_dict()

    def notify_shipment_created(self, shipment):
        """Notify the customer when a shipment is created."""
        message = build_shipment_created_message(shipment.tracking_id)
        self.create_notification(
            user_id=shipment.customer_id,
            message=message,
            shipment_id=shipment.id,
        )

    def notify_shipment_assigned(self, shipment, agent_id):
        """Notify the agent and customer when an agent is assigned."""
        tracking_id = shipment.tracking_id

        self.create_notification(
            user_id=agent_id,
            message=build_shipment_assigned_message(tracking_id, for_agent=True),
            shipment_id=shipment.id,
        )
        self.create_notification(
            user_id=shipment.customer_id,
            message=build_shipment_assigned_message(tracking_id, for_agent=False),
            shipment_id=shipment.id,
        )

    def notify_shipment_status_changed(self, shipment, new_status):
        """Notify relevant users when shipment status changes."""
        tracking_id = shipment.tracking_id

        if new_status == Shipment.STATUS_DELIVERED:
            self.create_notification(
                user_id=shipment.customer_id,
                message=build_delivered_message(tracking_id),
                shipment_id=shipment.id,
            )
        else:
            self.create_notification(
                user_id=shipment.customer_id,
                message=build_status_changed_message(tracking_id, new_status),
                shipment_id=shipment.id,
            )

        if shipment.agent_id:
            if new_status == Shipment.STATUS_DELIVERED:
                message = f'Shipment {tracking_id} has been marked as delivered.'
            else:
                message = build_status_changed_message(tracking_id, new_status)

            self.create_notification(
                user_id=shipment.agent_id,
                message=message,
                shipment_id=shipment.id,
            )
