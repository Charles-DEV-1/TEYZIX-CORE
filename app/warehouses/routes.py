"""
Warehouse API routes.
"""

from flask import Blueprint, jsonify, request

from app.middleware.auth_middleware import auth_required
from app.middleware.role_middleware import require_role
from app.warehouses.service import WarehouseService


warehouses_bp = Blueprint('warehouses', __name__, url_prefix='/warehouses')
warehouse_service = WarehouseService()


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


@warehouses_bp.route('', methods=['POST'])
@auth_required
@require_role('admin')
def create_warehouse(current_user):
    """
    Create warehouse
    ---
    tags:
      - Warehouses
    summary: Create a new warehouse (admin only)
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - location
            - capacity
          properties:
            name:
              type: string
              example: Lagos Main Hub
            location:
              type: string
              example: Lagos, Nigeria
            capacity:
              type: number
              example: 1000
    responses:
      201:
        description: Warehouse created successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Warehouse created successfully
            data:
              type: object
      400:
        description: Validation error
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    payload = request.get_json(silent=True) or {}

    try:
        warehouse = warehouse_service.create_warehouse(
            name=payload.get('name'),
            location=payload.get('location'),
            capacity=payload.get('capacity'),
        )
        return _json_response(True, 'Warehouse created successfully', warehouse, 201)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@warehouses_bp.route('', methods=['GET'])
@auth_required
def list_warehouses(current_user):
    """
    List warehouses
    ---
    tags:
      - Warehouses
    summary: List all warehouses with pagination
    security:
      - Bearer: []
    parameters:
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
        description: Warehouses retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Warehouses retrieved successfully
            data:
              type: object
      401:
        description: Authentication required
    """
    page = _parse_int(request.args.get('page'), 1)
    per_page = _parse_int(request.args.get('per_page'), 20)

    result = warehouse_service.list_warehouses(page=page, per_page=per_page)
    return _json_response(True, 'Warehouses retrieved successfully', result)


@warehouses_bp.route('/<int:warehouse_id>', methods=['GET'])
@auth_required
def get_warehouse(current_user, warehouse_id):
    """
    Get warehouse by ID
    ---
    tags:
      - Warehouses
    summary: Retrieve warehouse details
    security:
      - Bearer: []
    parameters:
      - in: path
        name: warehouse_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Warehouse details retrieved
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Warehouse details retrieved
            data:
              type: object
      404:
        description: Warehouse not found
      401:
        description: Authentication required
    """
    try:
        warehouse = warehouse_service.get_warehouse(warehouse_id)
        return _json_response(True, 'Warehouse details retrieved', warehouse)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=404)


@warehouses_bp.route('/<int:warehouse_id>', methods=['PUT'])
@auth_required
@require_role('admin')
def update_warehouse(current_user, warehouse_id):
    """
    Update warehouse
    ---
    tags:
      - Warehouses
    summary: Update warehouse details (admin only)
    security:
      - Bearer: []
    parameters:
      - in: path
        name: warehouse_id
        type: integer
        required: true
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Lagos Main Hub
            location:
              type: string
              example: Lagos, Nigeria
            capacity:
              type: number
              example: 1500
    responses:
      200:
        description: Warehouse updated successfully
      400:
        description: Validation error
      404:
        description: Warehouse not found
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    payload = request.get_json(silent=True) or {}

    try:
        warehouse = warehouse_service.update_warehouse(
            warehouse_id,
            **{key: payload[key] for key in ('name', 'location', 'capacity') if key in payload},
        )
        return _json_response(True, 'Warehouse updated successfully', warehouse)
    except ValueError as exc:
        status_code = 404 if str(exc) == 'Warehouse not found' else 400
        return _json_response(False, str(exc), status_code=status_code)


@warehouses_bp.route('/<int:warehouse_id>', methods=['DELETE'])
@auth_required
@require_role('admin')
def delete_warehouse(current_user, warehouse_id):
    """
    Delete warehouse
    ---
    tags:
      - Warehouses
    summary: Delete a warehouse (admin only)
    security:
      - Bearer: []
    parameters:
      - in: path
        name: warehouse_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Warehouse deleted successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Warehouse deleted successfully
      400:
        description: Warehouse has assigned shipments
      404:
        description: Warehouse not found
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    try:
        result = warehouse_service.delete_warehouse(warehouse_id)
        return _json_response(True, 'Warehouse deleted successfully', result)
    except ValueError as exc:
        status_code = 404 if str(exc) == 'Warehouse not found' else 400
        return _json_response(False, str(exc), status_code=status_code)


@warehouses_bp.route('/<int:warehouse_id>/shipments', methods=['GET'])
@auth_required
def get_warehouse_shipments(current_user, warehouse_id):
    """
    Get warehouse shipments
    ---
    tags:
      - Warehouses
    summary: List shipments stored in a warehouse
    security:
      - Bearer: []
    parameters:
      - in: path
        name: warehouse_id
        type: integer
        required: true
        example: 1
    responses:
      200:
        description: Warehouse shipments retrieved successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Warehouse shipments retrieved successfully
            data:
              type: array
              items:
                type: object
      404:
        description: Warehouse not found
      401:
        description: Authentication required
    """
    try:
        shipments = warehouse_service.get_warehouse_shipments(warehouse_id)
        return _json_response(True, 'Warehouse shipments retrieved successfully', shipments)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=404)
