# Flask Logistics Management API

A comprehensive, scalable Flask API for managing logistics operations including shipments, warehouses, delivery agents, and reporting.

## Project Overview

This project implements a clean, modular architecture designed for easy maintenance and feature expansion. The application follows best practices for Flask development with separation of concerns across different modules.

## Project Structure

```
project/
├── app/                          # Main application package
│   ├── __init__.py              # Application factory (create_app)
│   │
│   ├── auth/                    # Authentication module
│   │   ├── __init__.py
│   │   ├── routes.py            # Login, register, token endpoints
│   │   ├── service.py           # Authentication business logic
│   │   └── utils.py             # Auth utilities (validation, hashing)
│   │
│   ├── shipments/               # Shipment management module
│   │   ├── __init__.py
│   │   ├── routes.py            # Shipment CRUD endpoints
│   │   ├── service.py           # Shipment business logic
│   │   └── utils.py             # Shipment utilities
│   │
│   ├── warehouses/              # Warehouse management module
│   │   ├── __init__.py
│   │   ├── routes.py            # Warehouse endpoints
│   │   ├── service.py           # Warehouse business logic
│   │   └── utils.py             # Warehouse utilities
│   │
│   ├── delivery_agents/         # Delivery agent module
│   │   ├── __init__.py
│   │   ├── routes.py            # Agent endpoints
│   │   ├── service.py           # Agent business logic
│   │   └── utils.py             # Agent utilities
│   │
│   ├── reports/                 # Reporting module
│   │   ├── __init__.py
│   │   ├── routes.py            # Report endpoints
│   │   └── service.py           # Report generation logic
│   │
│   ├── notifications/           # Notification module
│   │   ├── __init__.py
│   │   ├── routes.py            # Notification endpoints
│   │   ├── service.py           # Notification logic
│   │   └── utils.py             # Email/SMS utilities
│   │
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── shipment.py          # Shipment model
│   │   ├── warehouse.py         # Warehouse model
│   │   ├── tracking.py          # Tracking events model
│   │   ├── notification.py      # Notification model
│   │   ├── refresh_token.py     # JWT refresh tokens
│   │   └── password_reset_token.py  # Password reset tokens
│   │
│   ├── middleware/              # Custom middleware
│   │   ├── __init__.py
│   │   ├── auth_middleware.py   # JWT authentication
│   │   └── role_middleware.py   # Role-based authorization
│   │
│   ├── extensions/              # Flask extensions
│   │   ├── __init__.py
│   │   ├── db.py                # SQLAlchemy database
│   │   ├── jwt.py               # JWT manager
│   │   ├── bcrypt.py            # Password hashing
│   │   └── redis.py             # Redis client
│   │
│   └── config/                  # Configuration management
│       ├── __init__.py
│       ├── base.py              # Base configuration
│       ├── development.py       # Development config
│       └── production.py        # Production config
│
├── app.py                       # Application entry point
├── config.py                    # Legacy config (reference only)
├── models.py                    # Legacy models (reference only)
├── routes/                      # Legacy routes (reference only)
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create locally)
├── .env.example                 # Environment template
└── README.md                    # This file

```

## Architecture Overview

### Module Organization

Each feature module (auth, shipments, warehouses, etc.) follows a consistent pattern:

- **routes.py**: Flask Blueprint with API endpoints
- **service.py**: Business logic implementation
- **utils.py**: Helper functions and utilities
- ****init**.py**: Module exports and configuration

### Extension Management

Extensions (database, JWT, etc.) are centralized in the `app/extensions/` module for clean initialization and reusability.

### Configuration

Environment-specific configuration is separated:

- Development config for local development
- Production config for deployed systems
- Base config with common settings

### Middleware

Custom middleware provides:

- JWT authentication (`auth_middleware.py`)
- Role-based authorization (`role_middleware.py`)

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (for caching)
- pip package manager

### Installation

1. **Clone the repository**

   ```bash
   cd project
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate      # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**

   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Initialize database**

   ```bash
   flask db upgrade
   ```

6. **Run development server**
   ```bash
   python app.py
   ```

## Configuration

### Environment Variables (.env)

```env
# Flask Settings
FLASK_ENV=development
FLASK_APP=app.py
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/logistics_db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-email-password

# Logging
LOG_LEVEL=INFO
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Logout user
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Complete password reset
- `GET /auth/me` - Get current user

### Shipments

- `POST /shipments` - Create shipment
- `GET /shipments` - List shipments
- `GET /shipments/<id>` - Get shipment details
- `PUT /shipments/<id>` - Update shipment
- `PATCH /shipments/<id>/status` - Update status
- `POST /shipments/<id>/assign-agent` - Assign agent
- `GET /shipments/<id>/tracking` - Get tracking history
- `DELETE /shipments/<id>` - Cancel shipment

### Warehouses

- `POST /warehouses` - Create warehouse
- `GET /warehouses` - List warehouses
- `GET /warehouses/<id>` - Get warehouse details
- `PUT /warehouses/<id>` - Update warehouse
- `DELETE /warehouses/<id>` - Delete warehouse
- `GET /warehouses/<id>/inventory` - Get inventory
- `GET /warehouses/<id>/shipments` - Get shipments
- `POST /warehouses/<id>/staff` - Add staff

### Delivery Agents

- `POST /agents` - Create agent
- `GET /agents` - List agents
- `GET /agents/<id>` - Get agent details
- `PUT /agents/<id>` - Update agent
- `GET /agents/<id>/shipments` - Get assigned shipments
- `PATCH /agents/<id>/status` - Update status
- `GET /agents/<id>/performance` - Get performance metrics
- `POST /agents/<id>/location` - Update GPS location

### Reports

- `GET /reports/shipments/summary` - Shipment summary
- `GET /reports/shipments/detailed` - Detailed shipment report
- `GET /reports/agents/performance` - Agent performance
- `GET /reports/warehouses/utilization` - Warehouse utilization
- `GET /reports/revenue/summary` - Revenue summary
- `GET /reports/trends/delivery-times` - Delivery trends
- `GET /reports/export/<type>` - Export report

### Notifications

- `GET /notifications` - Get notifications
- `GET /notifications/<id>` - Get notification
- `PATCH /notifications/<id>/read` - Mark as read
- `PATCH /notifications/read-all` - Mark all as read
- `DELETE /notifications/<id>` - Delete notification
- `GET /notifications/unread/count` - Unread count
- `POST /notifications/subscribe` - Subscribe

## Implementation Guide

### TODO Checklist for Developers

Before implementing features, follow this checklist:

1. **Models** (`app/models/`)
   - [ ] Define all database columns
   - [ ] Set up relationships
   - [ ] Add validators if needed
   - [ ] Create database migrations

2. **Services** (`app/*/service.py`)
   - [ ] Replace placeholder methods with implementations
   - [ ] Implement business logic
   - [ ] Add input validation
   - [ ] Handle error cases

3. **Routes** (`app/*/routes.py`)
   - [ ] Implement endpoint handlers
   - [ ] Add request validation
   - [ ] Add response formatting
   - [ ] Add error handlers

4. **Utilities** (`app/*/utils.py`)
   - [ ] Replace placeholder functions
   - [ ] Add input validation
   - [ ] Handle edge cases

5. **Middleware** (`app/middleware/`)
   - [ ] Implement authentication checks
   - [ ] Implement authorization checks
   - [ ] Add error handling

6. **Configuration** (`app/config/`)
   - [ ] Add environment variables
   - [ ] Set up extension configurations
   - [ ] Configure database connection

## Key Principles

### 1. Separation of Concerns

- Routes handle HTTP requests/responses
- Services handle business logic
- Utils handle reusable functions
- Models handle data structure

### 2. DRY (Don't Repeat Yourself)

- Reuse utils functions across services
- Centralize extension initialization
- Share middleware across routes

### 3. Configuration Management

- Use environment variables
- Keep sensitive data out of code
- Support multiple environments

### 4. Error Handling

- Validate inputs in services
- Return appropriate HTTP status codes
- Log errors appropriately

### 5. Documentation

- Include docstrings in all modules
- Document endpoint behavior
- Explain complex logic

## Running the Application

### Development

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python app.py

# Server runs on http://localhost:5000
```

### Production

```bash
# Using gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```

## Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app
```

## Database Migrations

```bash
# Create new migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

## API Documentation

Access API documentation at:

- Swagger UI: `http://localhost:5000/apidocs/`
- ReDoc: `http://localhost:5000/redoc/`

## Troubleshooting

### Database Connection Issues

- Verify DATABASE_URL in .env
- Check PostgreSQL is running
- Ensure database exists

### JWT Token Issues

- Verify JWT_SECRET_KEY is set
- Check token expiration settings
- Ensure proper header format

### Redis Connection Issues

- Verify Redis is running on localhost:6379
- Check REDIS_URL in .env
- Verify Redis credentials

## Contributing

1. Create feature branch
2. Implement changes following project structure
3. Add documentation and comments
4. Test thoroughly
5. Submit pull request

## License

[Add your license here]

## Support

For issues and questions:

- Create an issue in the repository
- Check existing documentation
- Review TODO comments in code

---

**Note:** This is a project template. All placeholder implementations marked with `TODO` should be completed before deployment.
