"""
QUICK START GUIDE
Flask Logistics Management API - Developer Onboarding

This guide helps new developers quickly understand the project structure
and start implementing features.
"""

# ============================================================================

# 1. PROJECT OVERVIEW

# ============================================================================

TECH STACK:

- Python 3.8+
- Flask 3.0+ (web framework)
- PostgreSQL 12+ (database)
- Redis (caching)
- SQLAlchemy (ORM)
- JWT (authentication)
- Flasgger (API documentation)

ARCHITECTURE:

- Modular: Each feature in its own module
- Service Layer: Business logic separated from routes
- Extensions: Centralized initialization
- Blueprints: Clean route organization

# ============================================================================

# 2. INITIAL SETUP

# ============================================================================

STEP 1: Clone and Navigate
cd project

STEP 2: Create Virtual Environment
python -m venv venv
source venv/Scripts/activate # Windows

# or

source venv/bin/activate # Linux/Mac

STEP 3: Install Dependencies
pip install -r requirements.txt

STEP 4: Create .env File
cp .env.example .env

# Edit .env with your database and service credentials

STEP 5: Create Database
createdb logistics_db

STEP 6: Run Migrations
flask db upgrade

STEP 7: Start Development Server
python app.py

# Server will be at http://localhost:5000

# ============================================================================

# 3. PROJECT FILE LOCATIONS

# ============================================================================

DATABASE MODELS:
Location: app/models/
Files: user.py, shipment.py, warehouse.py, etc.
Purpose: Define database schema

BUSINESS LOGIC (SERVICES):
Location: app/<feature>/service.py
Example: app/shipments/service.py
Purpose: Implement feature logic

API ROUTES:
Location: app/<feature>/routes.py
Example: app/shipments/routes.py
Purpose: Define API endpoints

HELPER FUNCTIONS:
Location: app/<feature>/utils.py
Example: app/shipments/utils.py
Purpose: Reusable utilities

MIDDLEWARE:
Location: app/middleware/
Files: auth_middleware.py, role_middleware.py
Purpose: Authentication and authorization

# ============================================================================

# 4. UNDERSTANDING THE MODULE STRUCTURE

# ============================================================================

Each Feature Module Contains:

app/
├── <feature>/
│ ├── **init**.py # Exports service and blueprint
│ ├── routes.py # API endpoints (Blueprint)
│ ├── service.py # Business logic (Service class)
│ └── utils.py # Helper functions

Example: Shipments Module

app/
├── shipments/
│ ├── **init**.py
│ │ # Exports: shipments_bp, ShipmentService, utils
│ │  
│ ├── routes.py
│ │ # Creates Blueprint: shipments_bp
│ │ # TODO: Implement endpoints like:
│ │ # @shipments_bp.route('', methods=['POST'])
│ │ # @shipments_bp.route('', methods=['GET'])
│ │ # @shipments_bp.route('/<id>', methods=['GET'])
│ │  
│ ├── service.py
│ │ # Class: ShipmentService
│ │ # TODO: Implement methods like:
│ │ # def create_shipment(...)
│ │ # def get_shipment(...)
│ │ # def list_shipments(...)
│ │  
│ └── utils.py
│ # TODO: Implement functions like:
│ # generate_shipment_id()
│ # validate_shipment_status()
│ # calculate_delivery_distance()

# ============================================================================

# 5. TYPICAL IMPLEMENTATION WORKFLOW

# ============================================================================

For a new feature (e.g., implementing Shipment Management):

STEP 1: Define the Model
File: app/models/shipment.py

class Shipment(db.Model):
**tablename** = 'shipments'

      id = db.Column(db.Integer, primary_key=True)
      shipment_id = db.Column(db.String(50), unique=True, nullable=False)
      status = db.Column(db.String(20), default='pending')
      weight = db.Column(db.Float)
      cost = db.Column(db.Float)
      created_at = db.Column(db.DateTime, default=datetime.utcnow)

STEP 2: Implement Service Layer
File: app/shipments/service.py

class ShipmentService:
def create_shipment(self, data): # Validate input # Create shipment record # Return created shipment

      def get_shipment(self, shipment_id):
          # Query shipment from database
          # Return shipment or raise 404

      def list_shipments(self, filters):
          # Query shipments with filters
          # Return paginated list

STEP 3: Create Routes
File: app/shipments/routes.py

from flask import request, jsonify
from .service import ShipmentService

shipments_bp = Blueprint('shipments', **name**, url_prefix='/shipments')
shipment_service = ShipmentService()

@shipments_bp.route('', methods=['POST'])
def create_shipment():
data = request.json
try:
shipment = shipment_service.create_shipment(data)
return jsonify(shipment), 201
except Exception as e:
return jsonify({'error': str(e)}), 400

STEP 4: Add Utilities
File: app/shipments/utils.py

def generate_shipment_id(): # Generate unique shipment ID
pass

def validate_shipment_status(status):
valid_statuses = ['pending', 'in_transit', 'delivered']
return status in valid_statuses

STEP 5: Register Blueprint
In: app/**init**.py create_app()

from app.shipments import shipments_bp
app.register_blueprint(shipments_bp)

# ============================================================================

# 6. COMMON CODE PATTERNS

# ============================================================================

PATTERN 1: Creating a Resource (POST)

@feature_bp.route('', methods=['POST'])
@auth_required # Require login
def create_resource():
data = request.json

    # Validate input
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400

    # Call service
    try:
        resource = service.create_resource(data)
        return jsonify(resource), 201
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

PATTERN 2: Getting a Resource (GET)

@feature_bp.route('/<int:resource_id>', methods=['GET'])
@auth_required
def get_resource(resource_id):
try:
resource = service.get_resource(resource_id)
if not resource:
return jsonify({'error': 'Not found'}), 404
return jsonify(resource), 200
except Exception as e:
return jsonify({'error': str(e)}), 500

PATTERN 3: Listing Resources (GET)

@feature_bp.route('', methods=['GET'])
@auth_required
def list_resources():
page = request.args.get('page', 1, type=int)
per_page = request.args.get('per_page', 20, type=int)

    resources = service.list_resources(page=page, per_page=per_page)
    return jsonify(resources), 200

PATTERN 4: Updating a Resource (PUT)

@feature_bp.route('/<int:resource_id>', methods=['PUT'])
@auth_required
def update_resource(resource_id):
data = request.json

    try:
        resource = service.update_resource(resource_id, data)
        return jsonify(resource), 200
    except NotFound:
        return jsonify({'error': 'Not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

PATTERN 5: Deleting a Resource (DELETE)

@feature_bp.route('/<int:resource_id>', methods=['DELETE'])
@auth_required
@require_role('admin') # Only admin can delete
def delete_resource(resource_id):
try:
service.delete_resource(resource_id)
return '', 204
except NotFound:
return jsonify({'error': 'Not found'}), 404
except Exception as e:
return jsonify({'error': str(e)}), 500

# ============================================================================

# 7. DATABASE OPERATIONS IN SERVICE LAYER

# ============================================================================

QUERYING DATA:

from app.models import Shipment
from app.extensions import db

# Get single record

shipment = Shipment.query.get(1)
shipment = Shipment.query.filter_by(shipment_id='SHP001').first()

# Get multiple records

shipments = Shipment.query.all()
shipments = Shipment.query.filter_by(status='pending').all()

# Paginated query

page = request.args.get('page', 1, type=int)
paginated = Shipment.query.paginate(page=page, per_page=20)

CREATING DATA:

shipment = Shipment(
shipment_id='SHP001',
status='pending',
weight=10.5,
cost=100.0
)
db.session.add(shipment)
db.session.commit()

UPDATING DATA:

shipment = Shipment.query.get(1)
shipment.status = 'in_transit'
db.session.commit()

DELETING DATA:

shipment = Shipment.query.get(1)
db.session.delete(shipment)
db.session.commit()

# ============================================================================

# 8. AUTHENTICATION & AUTHORIZATION

# ============================================================================

PROTECTING ROUTES:

from app.middleware import auth_required, require_role

@shipments_bp.route('', methods=['POST'])
@auth_required # User must be logged in
def create_shipment():
pass

@shipments_bp.route('/<id>', methods=['DELETE'])
@auth_required # Must be logged in
@require_role('admin') # Must be admin
def delete_shipment(id):
pass

GETTING CURRENT USER IN ROUTE:

from flask_jwt_extended import get_jwt_identity

@shipments_bp.route('/my-shipments', methods=['GET'])
@auth_required
def get_my_shipments():
current_user_id = get_jwt_identity()
shipments = service.get_user_shipments(current_user_id)
return jsonify(shipments), 200

# ============================================================================

# 9. COMMON GOTCHAS & TIPS

# ============================================================================

TIP 1: Always validate input data before processing
✓ Check required fields exist
✓ Validate data types
✓ Check value ranges
✓ Return 400 Bad Request if invalid

TIP 2: Use HTTP status codes correctly
✓ 200 OK - Successful GET, PUT, PATCH
✓ 201 Created - Successful POST
✓ 204 No Content - Successful DELETE
✓ 400 Bad Request - Invalid input
✓ 401 Unauthorized - Authentication required
✓ 403 Forbidden - Authorization failed
✓ 404 Not Found - Resource doesn't exist
✓ 500 Internal Server Error - Unexpected error

TIP 3: Always use database sessions carefully
✓ Use try/except for database operations
✓ Rollback on error
✓ Commit only after successful operations

TIP 4: Test each endpoint as you implement
✓ Use curl or Postman
✓ Test happy path (success)
✓ Test error cases
✓ Test edge cases

TIP 5: Keep business logic in service layer
✗ WRONG: Putting DB queries in route handler
✓ RIGHT: Route calls service which queries DB

TIP 6: Document complex logic with comments
✓ Explain WHY, not WHAT
✓ Include examples for complex operations
✓ Reference related code

# ============================================================================

# 10. USEFUL COMMANDS

# ============================================================================

Development Server:
python app.py # Start dev server
python app.py --debug # Start with debug reloader

Database:
flask db init # Initialize migrations
flask db migrate -m "message" # Create migration
flask db upgrade # Apply migrations
flask db downgrade # Rollback migration

Testing:
pytest # Run all tests
pytest tests/test_shipments.py # Run specific test file
pytest -v # Verbose output
pytest --cov=app # With coverage

Dependencies:
pip install -r requirements.txt # Install all packages
pip freeze > requirements.txt # Update requirements file

API Documentation:

# Visit http://localhost:5000/apidocs/

# ============================================================================

# 11. ASKING FOR HELP

# ============================================================================

When stuck:

1. Check TODO comments in the code
2. Look at similar implemented features
3. Check the docstrings
4. Review PROJECT_STRUCTURE.md
5. Check the README.md

Common Issues:

- ModuleNotFoundError: Ensure import paths are correct
- 404 errors: Check blueprint url_prefix
- Authentication errors: Verify JWT token format
- Database errors: Check .env DATABASE_URL

# ============================================================================

# 12. NEXT STEPS

# ============================================================================

1. Read PROJECT_STRUCTURE.md for architecture overview
2. Review one complete feature (e.g., auth/) for pattern understanding
3. Start implementing the first feature
4. Test each endpoint as you build it
5. Move to the next feature

Start with simpler features first:

1. Auth (essential for other features)
2. Warehouses (no dependencies)
3. Shipments (depends on warehouses)
4. Delivery Agents (depends on warehouses)
5. Reports (depends on shipments and agents)
6. Notifications (depends on other features)

Happy coding!
"""
