"""
Shipments Routes Module
"""

from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import auth_required
from app.shipments.service import ShipmentService
from app.warehouses.service import WarehouseService

shipments_bp = Blueprint('shipments', __name__, url_prefix='/shipments')
shipment_service = ShipmentService()
warehouse_service = WarehouseService()


def _json_response(success: bool, message: str, data=None, status_code: int = 200):
    response = {'success': success, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def _parse_int(value, default=1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@shipments_bp.route('', methods=['POST'])
@auth_required
def create_shipment(current_user):
    """
    Create shipment
    ---
    tags:
      - Shipments
    summary: Create a new shipment
    description: Authenticated user becomes the customer for the shipment.
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - sender_name
            - sender_phone
            - receiver_name
            - receiver_phone
            - package_type
            - weight
            - delivery_address
          properties:
            sender_name:
              type: string
              example: Alice Sender
            sender_phone:
              type: string
              example: '+1234567890'
            receiver_name:
              type: string
              example: Bob Receiver
            receiver_phone:
              type: string
              example: '+0987654321'
            package_type:
              type: string
              example: parcel
            weight:
              type: number
              example: 2.5
            delivery_address:
              type: string
              example: 123 Main St, Lagos
            warehouse_id:
              type: integer
              example: 1
            assigned_agent_id:
              type: integer
              example: 3
    responses:
      201:
        description: Shipment created successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Shipment created successfully
            data:
              type: object
      400:
        description: Validation error
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Weight must be greater than zero
      401:
        description: Authentication required
    """
    payload = request.get_json(silent=True) or {}
    try:
        shipment = shipment_service.create_shipment(
            sender_name=payload.get('sender_name'),
            sender_phone=payload.get('sender_phone'),
            receiver_name=payload.get('receiver_name'),
            receiver_phone=payload.get('receiver_phone'),
            package_type=payload.get('package_type'),
            weight=payload.get('weight'),
            delivery_address=payload.get('delivery_address'),
            customer_id=current_user.id,
            warehouse_id=payload.get('warehouse_id'),
            assigned_agent_id=payload.get('assigned_agent_id'),
        )
        return _json_response(True, 'Shipment created successfully', shipment, 201)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@shipments_bp.route('', methods=['GET'])
@auth_required
def list_shipments(current_user):
    """
    List shipments
    ---
    tags:
      - Shipments
    summary: List shipments with optional filters
    security:
      - Bearer: []
    parameters:
      - in: query
        name: status
        type: string
        enum: [CREATED, PICKED_UP, IN_WAREHOUSE, OUT_FOR_DELIVERY, DELIVERED]
        example: CREATED
      - in: query
        name: tracking_id
        type: string
        example: SHP
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
        description: Shipments retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Shipments retrieved successfully
            data:
              type: object
              properties:
                items:
                  type: array
                  items:
                    type: object
                meta:
                  type: object
      400:
        description: Invalid filter
      401:
        description: Authentication required
    """
    status = request.args.get('status')
    tracking_id = request.args.get('tracking_id')
    page = _parse_int(request.args.get('page'), 1)
    per_page = _parse_int(request.args.get('per_page'), 20)

    try:
        result = shipment_service.list_shipments(
            status=status,
            tracking_id=tracking_id,
            page=page,
            per_page=per_page,
        )
        return _json_response(True, 'Shipments retrieved successfully', result)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@shipments_bp.route('/<int:shipment_id>', methods=['GET'])
@auth_required
def get_shipment(current_user, shipment_id):
    """
    Get shipment by ID
    ---
    tags:
      - Shipments
    summary: Retrieve shipment details including tracking history
    security:
      - Bearer: []
    parameters:
      - in: path
        name: shipment_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Shipment details retrieved
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Shipment details retrieved
            data:
              type: object
      404:
        description: Shipment not found
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: Shipment not found
      401:
        description: Authentication required
    """
    try:
        shipment = shipment_service.get_shipment(shipment_id)
        return _json_response(True, 'Shipment details retrieved', shipment)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=404)


@shipments_bp.route('/search', methods=['GET'])
@auth_required
def search_shipments(current_user):
    """
    Search shipments
    ---
    tags:
      - Shipments
    summary: Search shipments by tracking ID
    security:
      - Bearer: []
    parameters:
      - in: query
        name: tracking_id
        type: string
        required: true
        example: SHP20260101120000ABC123
      - in: query
        name: status
        type: string
        enum: [CREATED, PICKED_UP, IN_WAREHOUSE, OUT_FOR_DELIVERY, DELIVERED]
      - in: query
        name: page
        type: integer
        default: 1
      - in: query
        name: per_page
        type: integer
        default: 20
    responses:
      200:
        description: Search completed
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Shipment search completed
            data:
              type: object
      400:
        description: Tracking ID is required or invalid filter
      401:
        description: Authentication required
    """
    tracking_id = request.args.get('tracking_id')
    status = request.args.get('status')
    page = _parse_int(request.args.get('page'), 1)
    per_page = _parse_int(request.args.get('per_page'), 20)

    try:
        result = shipment_service.search_shipments(
            tracking_id=tracking_id,
            status=status,
            page=page,
            per_page=per_page,
        )
        return _json_response(True, 'Shipment search completed', result)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@shipments_bp.route('/track/<tracking_id>', methods=['GET'])
@auth_required
def track_shipment(current_user, tracking_id):
    """
    Track shipment
    ---
    tags:
      - Shipments
    summary: Track a shipment by its tracking ID
    security:
      - Bearer: []
    parameters:
      - in: path
        name: tracking_id
        type: string
        required: true
        example: SHP20260101120000ABC123
    responses:
      200:
        description: Tracking information retrieved
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Tracking information retrieved
            data:
              type: object
      404:
        description: Shipment not found
      401:
        description: Authentication required
    """
    try:
        shipment = shipment_service.track_shipment(tracking_id)
        return _json_response(True, 'Tracking information retrieved', shipment)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=404)


@shipments_bp.route('/<int:shipment_id>/assign-warehouse', methods=['PUT'])
@auth_required
def assign_warehouse(current_user, shipment_id):
    """
    Assign shipment to warehouse
    ---
    tags:
      - Shipments
    summary: Assign a shipment to a warehouse
    security:
      - Bearer: []
    parameters:
      - in: path
        name: shipment_id
        type: integer
        required: true
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - warehouse_id
          properties:
            warehouse_id:
              type: integer
              example: 1
    responses:
      200:
        description: Shipment assigned to warehouse successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Shipment assigned to warehouse successfully
            data:
              type: object
      400:
        description: Validation error or insufficient warehouse capacity
      404:
        description: Shipment or warehouse not found
      401:
        description: Authentication required
    """
    payload = request.get_json(silent=True) or {}
    warehouse_id = payload.get('warehouse_id')

    try:
        shipment = warehouse_service.assign_shipment_to_warehouse(
            shipment_id=shipment_id,
            warehouse_id=warehouse_id,
        )
        return _json_response(True, 'Shipment assigned to warehouse successfully', shipment)
    except ValueError as exc:
        status_code = 404 if str(exc) in {'Shipment not found', 'Warehouse not found'} else 400
        return _json_response(False, str(exc), status_code=status_code)
