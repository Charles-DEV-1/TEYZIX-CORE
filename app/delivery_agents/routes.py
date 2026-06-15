"""
Delivery Agents Routes Module
"""

from flask import Blueprint, request, jsonify
from app.middleware.auth_middleware import auth_required
from app.middleware.role_middleware import require_role
from app.delivery_agents.service import AgentService

agent_bp = Blueprint('agent', __name__, url_prefix='/agent')
agent_shipments_bp = Blueprint('agent_shipments', __name__, url_prefix='/shipments')

agent_service = AgentService()

# Backward-compatible alias used by app factory
agents_bp = agent_bp


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


@agent_bp.route('/shipments', methods=['GET'])
@auth_required
@require_role('delivery_agent')
def list_agent_shipments(current_user):
    """
    List assigned shipments
    ---
    tags:
      - Delivery Agents
    summary: List shipments assigned to the logged-in delivery agent
    security:
      - Bearer: []
    parameters:
      - in: query
        name: status
        type: string
        enum: [CREATED, PICKED_UP, IN_WAREHOUSE, OUT_FOR_DELIVERY, DELIVERED]
        example: OUT_FOR_DELIVERY
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
        description: Assigned shipments retrieved
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Assigned shipments retrieved
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
        description: Invalid status filter
      401:
        description: Authentication required
      403:
        description: Delivery agent role required
    """
    status = request.args.get('status')
    page = _parse_int(request.args.get('page'), 1)
    per_page = _parse_int(request.args.get('per_page'), 20)

    try:
        result = agent_service.list_assigned_shipments(
            agent_id=current_user.id,
            status=status,
            page=page,
            per_page=per_page,
        )
        return _json_response(True, 'Assigned shipments retrieved', result)
    except ValueError as exc:
        return _json_response(False, str(exc), status_code=400)


@agent_shipments_bp.route('/<int:shipment_id>/assign-agent', methods=['PUT'])
@auth_required
@require_role('admin')
def assign_agent(current_user, shipment_id):
    """
    Assign delivery agent
    ---
    tags:
      - Delivery Agents
    summary: Assign a delivery agent to a shipment (admin only)
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
            - agent_id
          properties:
            agent_id:
              type: integer
              example: 3
    responses:
      200:
        description: Agent assigned successfully
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Agent assigned successfully
            data:
              type: object
      400:
        description: Agent ID is required
      404:
        description: Shipment or delivery agent not found
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    payload = request.get_json(silent=True) or {}
    agent_id = payload.get('agent_id')

    try:
        shipment = agent_service.assign_agent_to_shipment(
            shipment_id=shipment_id,
            agent_id=agent_id,
        )
        return _json_response(True, 'Agent assigned successfully', shipment)
    except ValueError as exc:
        status_code = 404 if str(exc) in {'Shipment not found', 'Delivery agent not found'} else 400
        return _json_response(False, str(exc), status_code=status_code)


@agent_shipments_bp.route('/<int:shipment_id>/status', methods=['PUT'])
@auth_required
@require_role('admin', 'delivery_agent')
def update_shipment_status(current_user, shipment_id):
    """
    Update shipment status
    ---
    tags:
      - Delivery Agents
    summary: Update shipment status (admin or assigned agent)
    description: Agents can only update shipments assigned to them.
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
            - status
          properties:
            status:
              type: string
              enum: [PICKED_UP, IN_WAREHOUSE, OUT_FOR_DELIVERY, DELIVERED]
              example: OUT_FOR_DELIVERY
    responses:
      200:
        description: Shipment status updated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Shipment status updated
            data:
              type: object
      400:
        description: Invalid status or invalid transition
      403:
        description: Agent trying to update unassigned shipment
      404:
        description: Shipment not found
      401:
        description: Authentication required
    """
    payload = request.get_json(silent=True) or {}
    new_status = payload.get('status')

    try:
        shipment = agent_service.update_shipment_status(
            shipment_id=shipment_id,
            new_status=new_status,
            current_user=current_user,
        )
        return _json_response(True, 'Shipment status updated', shipment)
    except ValueError as exc:
        if str(exc) == 'Forbidden':
            return _json_response(False, str(exc), status_code=403)
        if str(exc) == 'Shipment not found':
            return _json_response(False, str(exc), status_code=404)
        return _json_response(False, str(exc), status_code=400)


@agent_shipments_bp.route('/<int:shipment_id>/proof', methods=['POST'])
@auth_required
@require_role('delivery_agent')
def submit_delivery_proof(current_user, shipment_id):
    """
    Submit delivery proof
    ---
    tags:
      - Delivery Agents
    summary: Submit proof of delivery for an assigned shipment
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
            - proof_text
          properties:
            proof_text:
              type: string
              example: Delivered to receiver at front door, signed by John
    responses:
      201:
        description: Delivery proof submitted
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Delivery proof submitted
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                shipment_id:
                  type: integer
                  example: 1
                proof_text:
                  type: string
                created_at:
                  type: string
      400:
        description: Proof text is required
      403:
        description: Shipment not assigned to agent
      404:
        description: Shipment not found
      401:
        description: Authentication required
    """
    payload = request.get_json(silent=True) or {}
    proof_text = payload.get('proof_text')

    try:
        proof = agent_service.submit_delivery_proof(
            shipment_id=shipment_id,
            proof_text=proof_text,
            current_user=current_user,
        )
        return _json_response(True, 'Delivery proof submitted', proof, 201)
    except ValueError as exc:
        if str(exc) == 'Forbidden':
            return _json_response(False, str(exc), status_code=403)
        if str(exc) == 'Shipment not found':
            return _json_response(False, str(exc), status_code=404)
        return _json_response(False, str(exc), status_code=400)
