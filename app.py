"""
Flask Application Entry Point

PURPOSE:
    Serve as the entry point for running the Flask application.
    Create app instance and start development server.

USAGE:
    Development:
        python app.py
        
    Production:
        gunicorn -w 4 -b 0.0.0.0:5000 'app:app'

TODO - Implementation:
    1. Import create_app from app package
    2. Create app instance using factory
    3. Add health check route
    4. Run development server on port 5000
"""

import os
from app import create_app

config_name = 'production' if os.getenv('FLASK_ENV') == 'production' else 'development'
app = create_app(config_name)

if __name__ == '__main__':
    # Run development server
    app.run(debug=True, host='0.0.0.0', port=5000)
