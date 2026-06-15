"""
Flask Logistics Management API Application Factory

PURPOSE:
    Create and configure the Flask application instance.
    Initialize extensions and register blueprints.
    Serve as the entry point for the entire application.

RESPONSIBILITIES:
    - Create Flask app instance
    - Load configuration
    - Initialize extensions
    - Register blueprints
    - Set up error handlers
    - Configure logging
    - Set up Swagger/API documentation

WHEN TO USE:
    - Call create_app() to instantiate the application
    - Used in wsgi.py for production servers
    - Used in development server startup

WHAT NOT TO PUT HERE:
    - Business logic
    - Route handlers (define in blueprint modules)
    - Database models (define in models/)
    - Configuration logic (handle in config/)

APPLICATION STRUCTURE:
    Flask app with modular blueprints for:
    - Authentication (auth/)
    - Shipments (shipments/)
    - Warehouses (warehouses/)
    - Delivery Agents (delivery_agents/)
    - Reports (reports/)
    - Notifications (notifications/)

TODO - Implementation steps:
    1. Configure Flask app with config object
    2. Initialize database connection
    3. Initialize JWT manager
    4. Initialize Bcrypt
    5. Initialize Redis connection
    6. Register all blueprints with url_prefix
    7. Set up error handlers
    8. Configure logging
    9. Initialize Swagger/Flasgger documentation
    10. Add health check endpoint
"""

from flask import Flask
from flask_cors import CORS
import flask_migrate
try:
    from flasgger import Flasgger
except Exception:
    Flasgger = None
from flask_migrate import Migrate

# Import extensions and configurations
from app.config import DevelopmentConfig, ProductionConfig


def create_app(config_name='development'):
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment ('development' or 'production')
    
    Returns:
        Configured Flask application instance
    
    TODO: Implement app factory logic
    
    Steps:
    1. Create Flask app instance
    2. Load configuration based on config_name
    3. Initialize extensions with app
    4. Register blueprints
    5. Set up error handlers
    6. Initialize Swagger documentation
    7. Configure CORS
    8. Return app instance
    """
    
    # Create Flask application
    app = Flask(__name__, instance_relative_config=False)

    # Load configuration
    if config_name == 'production':
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    try:
        from app.extensions.redis import init_redis
        init_redis(
            require_connection=app.config.get('REQUIRE_REDIS', False),
            redis_url=app.config.get('REDIS_URL'),
        )
    except RuntimeError:
        raise

    # Initialize extensions (import inside factory to avoid import-time failures)
    try:
        from app.extensions import db, jwt, bcrypt, redis_client
    except Exception:
        db = None
        jwt = None
        bcrypt = None
        redis_client = None

    if db is not None:
        db.init_app(app)
        # Import models after db is initialized so SQLAlchemy metadata is populated.
        try:
            import importlib
            importlib.import_module('app.models')
        except Exception:
            pass

    if jwt is not None:
        jwt.init_app(app)

    # Initialize Flask-Migrate using shared migrate instance
    try:
        from app.extensions import migrate
        if db is not None:
            migrate.init_app(app, db)
    except Exception:
        pass

    if jwt is not None:
        @jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload):
            from app.extensions.redis import redis_client
            if redis_client is None:
                return False
            jti = jwt_payload.get('jti')
            if not jti:
                return False
            return redis_client.exists(f'jwt_blocklist:{jti}') == 1

        @jwt.revoked_token_loader
        def revoked_token_callback(jwt_header, jwt_payload):
            from flask import jsonify
            return jsonify({'success': False, 'message': 'Token has been revoked'}), 401

    # Enable CORS
    CORS(app)

    # Register blueprints (import here so they can access initialized extensions)
    try:
        from app.auth import auth_bp
        from app.shipments import shipments_bp
        from app.warehouses import warehouses_bp
        from app.delivery_agents import agents_bp, agent_shipments_bp
        from app.reports import reports_bp
        from app.notifications import notifications_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(shipments_bp)
        app.register_blueprint(warehouses_bp)
        app.register_blueprint(agents_bp)
        app.register_blueprint(agent_shipments_bp)
        app.register_blueprint(reports_bp)
        app.register_blueprint(notifications_bp)
    except Exception:
        # Blueprints optional during initial migration setup
        pass

    # Initialize Swagger (Flasgger) after blueprints so all routes are documented
    try:
        from app.swagger_config import SWAGGER_CONFIG, SWAGGER_TEMPLATE
        Flasgger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)
    except Exception:
        # Flasgger optional during initial setup
        pass

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Health check
        ---
        tags:
          - Health
        summary: Check API and Redis health
        description: No authentication required.
        responses:
          200:
            description: Service is healthy
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: healthy
                redis:
                  type: string
                  example: connected
          503:
            description: Service unhealthy (Redis required but disconnected in production)
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: unhealthy
                redis:
                  type: string
                  example: disconnected
        """
        status = {'status': 'healthy'}
        try:
            from app.extensions.redis import redis_client
            if redis_client is not None:
                redis_client.ping()
                status['redis'] = 'connected'
            else:
                status['redis'] = 'unavailable'
        except Exception:
            status['redis'] = 'disconnected'
            if app.config.get('REQUIRE_REDIS'):
                return {'status': 'unhealthy', 'redis': 'disconnected'}, 503
        return status, 200

    return app


# TODO: Create entry point for development server
# if __name__ == '__main__':
#     app = create_app('development')
#     app.run(debug=True, host='0.0.0.0', port=5000)

# NOTE: For production, use:
# gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
