"""
Notifications Routes Module
"""

from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import auth_required
from app.notifications.service import NotificationService

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')
notification_service = NotificationService()


def _json_response(success, message, data=None, status_code=200):
    response = {'success': success, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def _parse_int(value, default=1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_bool(value):
    if value is None:
        return None
    return value.lower() in ('true', '1', 'yes')


@notifications_bp.route('', methods=['GET'])
@auth_required
def get_notifications(current_user):
    """
    List notifications
    ---
    tags:
      - Notifications
    summary: Get notifications for the authenticated user
    security:
      - Bearer: []
    parameters:
      - in: query
        name: is_read
        type: boolean
        description: Filter by read status (true or false)
        example: false
      - in: query
        name: page
        type: integer
        default: 1
        example: 1
      - in: query
        name: per_page
        type: integer
        default: 20
        example: 20
    responses:
      200:
        description: Notifications retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Notifications retrieved successfully
            data:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      user_id:
                        type: integer
                        example: 2
                      shipment_id:
                        type: integer
                        example: 3
                      message:
                        type: string
                        example: Your shipment SHP20260101120000ABC123 has been created successfully.
                      is_read:
                        type: boolean
                        example: false
                      created_at:
                        type: string
                        example: '2026-06-14T12:00:00'
                meta:
                  type: object
      401:
        description: Authentication required
    """
    is_read = _parse_bool(request.args.get('is_read'))
    page = _parse_int(request.args.get('page'), 1)
    per_page = _parse_int(request.args.get('per_page'), 20)

    result = notification_service.get_user_notifications(
        user_id=current_user.id,
        is_read=is_read,
        page=page,
        per_page=per_page,
    )
    return _json_response(True, 'Notifications retrieved successfully', result)


@notifications_bp.route('/<int:notification_id>/read', methods=['PUT'])
@auth_required
def mark_notification_read(current_user, notification_id):
    """
    Mark notification as read
    ---
    tags:
      - Notifications
    summary: Mark a single notification as read
    security:
      - Bearer: []
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Notification marked as read
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Notification marked as read
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                is_read:
                  type: boolean
                  example: true
      404:
        description: Notification not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Notification not found
      401:
        description: Authentication required
    """
    try:
        notification = notification_service.mark_as_read(
            notification_id=notification_id,
            user_id=current_user.id,
        )
        return _json_response(True, 'Notification marked as read', notification)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=404)
