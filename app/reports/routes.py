"""
Reports Routes Module
"""

from flask import Blueprint, jsonify
from app.middleware.auth_middleware import auth_required
from app.middleware.role_middleware import require_role
from app.reports.service import ReportService

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
report_service = ReportService()


def _json_response(success, message, data=None, status_code=200):
    response = {'success': success, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


@reports_bp.route('/daily-shipments', methods=['GET'])
@auth_required
@require_role('admin')
def daily_shipments_report(current_user):
    """
    Daily shipments report
    ---
    tags:
      - Reports
    summary: Report shipments created today (admin only)
    security:
      - Bearer: []
    responses:
      200:
        description: Daily shipments report generated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Daily shipments report generated
            data:
              type: object
              properties:
                date:
                  type: string
                  example: '2026-06-14'
                total_shipments:
                  type: integer
                  example: 5
                delivered_shipments:
                  type: integer
                  example: 1
                pending_shipments:
                  type: integer
                  example: 4
                shipments:
                  type: array
                  items:
                    type: object
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    report = report_service.get_daily_shipments()
    return _json_response(True, 'Daily shipments report generated', report)


@reports_bp.route('/delivered', methods=['GET'])
@auth_required
@require_role('admin')
def delivered_report(current_user):
    """
    Delivered shipments report
    ---
    tags:
      - Reports
    summary: Report all delivered shipments (admin only)
    security:
      - Bearer: []
    responses:
      200:
        description: Delivered shipments report generated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Delivered shipments report generated
            data:
              type: object
              properties:
                total_shipments:
                  type: integer
                  example: 20
                delivered_shipments:
                  type: integer
                  example: 8
                pending_shipments:
                  type: integer
                  example: 12
                shipments:
                  type: array
                  items:
                    type: object
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    report = report_service.get_delivered_report()
    return _json_response(True, 'Delivered shipments report generated', report)


@reports_bp.route('/pending', methods=['GET'])
@auth_required
@require_role('admin')
def pending_report(current_user):
    """
    Pending shipments report
    ---
    tags:
      - Reports
    summary: Report all non-delivered shipments (admin only)
    security:
      - Bearer: []
    responses:
      200:
        description: Pending shipments report generated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Pending shipments report generated
            data:
              type: object
              properties:
                total_shipments:
                  type: integer
                  example: 20
                delivered_shipments:
                  type: integer
                  example: 8
                pending_shipments:
                  type: integer
                  example: 12
                shipments:
                  type: array
                  items:
                    type: object
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    report = report_service.get_pending_report()
    return _json_response(True, 'Pending shipments report generated', report)


@reports_bp.route('/warehouse-utilization', methods=['GET'])
@auth_required
@require_role('admin')
def warehouse_utilization_report(current_user):
    """
    Warehouse utilization report
    ---
    tags:
      - Reports
    summary: Report warehouse capacity utilization (admin only)
    security:
      - Bearer: []
    responses:
      200:
        description: Warehouse utilization report generated
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: Warehouse utilization report generated
            data:
              type: object
              properties:
                total_shipments:
                  type: integer
                  example: 20
                delivered_shipments:
                  type: integer
                  example: 8
                pending_shipments:
                  type: integer
                  example: 12
                overall_utilization_percentage:
                  type: number
                  example: 45.5
                warehouses:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Lagos Main Hub
                      utilization_percentage:
                        type: number
                        example: 45.5
      401:
        description: Authentication required
      403:
        description: Admin role required
    """
    report = report_service.get_warehouse_utilization()
    return _json_response(True, 'Warehouse utilization report generated', report)
