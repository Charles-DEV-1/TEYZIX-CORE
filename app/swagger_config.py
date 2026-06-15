"""
Flasgger / Swagger configuration for API documentation.
"""

SWAGGER_CONFIG = {
    'headers': [],
    'specs': [
        {
            'endpoint': 'apispec',
            'route': '/apispec.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/apidocs/',
}

SWAGGER_TEMPLATE = {
    'swagger': '2.0',
    'info': {
        'title': 'Logistics Management API',
        'description': (
            'REST API for logistics shipment management, warehouses, '
            'delivery agents, notifications, and reports.'
        ),
        'version': '1.0.0',
    },
    'securityDefinitions': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT access token. Format: Bearer <access_token>',
        },
        'RefreshToken': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT refresh token. Format: Bearer <refresh_token>',
        },
    },
    'tags': [
        {'name': 'Health', 'description': 'Service health checks'},
        {'name': 'Auth', 'description': 'Authentication and user management'},
        {'name': 'Shipments', 'description': 'Shipment creation and tracking'},
        {'name': 'Warehouses', 'description': 'Warehouse management'},
        {'name': 'Delivery Agents', 'description': 'Agent assignments and delivery operations'},
        {'name': 'Notifications', 'description': 'User notifications'},
        {'name': 'Reports', 'description': 'Admin reports and analytics'},
    ],
}
