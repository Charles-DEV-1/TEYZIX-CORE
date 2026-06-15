"""
Shared pytest fixtures for API integration tests.
"""

import pytest
from sqlalchemy.pool import StaticPool

from app import create_app
from app.extensions import db

TEST_PASSWORD = 'SecurePass1!'


@pytest.fixture
def app():
    """Create a Flask app with an in-memory SQLite database."""
    application = create_app('testing')
    application.config.update(
        SQLALCHEMY_ENGINE_OPTIONS={
            'connect_args': {'check_same_thread': False},
            'poolclass': StaticPool,
        }
    )

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Flask test client."""
    return app.test_client()


def register_user(client, name, email, role='customer'):
    """Helper to register a user."""
    return client.post(
        '/auth/register',
        json={
            'name': name,
            'email': email,
            'password': TEST_PASSWORD,
            'role': role,
        },
    )


def login_user(client, email):
    """Helper to log in and return the JSON response."""
    return client.post(
        '/auth/login',
        json={
            'email': email,
            'password': TEST_PASSWORD,
        },
    )


def auth_headers(access_token):
    """Build Authorization headers from an access token."""
    return {'Authorization': f'Bearer {access_token}'}


@pytest.fixture
def customer(client):
    """Registered customer with a valid access token."""
    email = 'customer@test.com'
    register_user(client, 'Test Customer', email, 'customer')
    response = login_user(client, email)
    tokens = response.get_json()['data']

    return {
        'email': email,
        'tokens': tokens,
        'headers': auth_headers(tokens['access_token']),
        'refresh_headers': auth_headers(tokens['refresh_token']),
    }


@pytest.fixture
def admin(client):
    """Registered admin with a valid access token."""
    email = 'admin@test.com'
    register_user(client, 'Test Admin', email, 'admin')
    response = login_user(client, email)
    tokens = response.get_json()['data']

    return {
        'email': email,
        'tokens': tokens,
        'headers': auth_headers(tokens['access_token']),
    }


@pytest.fixture
def agent(client):
    """Registered delivery agent with a valid access token."""
    email = 'agent@test.com'
    register_user(client, 'Test Agent', email, 'delivery_agent')
    response = login_user(client, email)
    tokens = response.get_json()['data']

    return {
        'email': email,
        'user_id': tokens['user']['id'],
        'tokens': tokens,
        'headers': auth_headers(tokens['access_token']),
    }


@pytest.fixture
def sample_shipment(client, customer):
    """Create a shipment and return its data."""
    response = client.post(
        '/shipments',
        json={
            'sender_name': 'Alice Sender',
            'sender_phone': '+1111111111',
            'receiver_name': 'Bob Receiver',
            'receiver_phone': '+2222222222',
            'package_type': 'parcel',
            'weight': 2.5,
            'delivery_address': '123 Test Street',
        },
        headers=customer['headers'],
    )
    return response.get_json()['data']


@pytest.fixture
def sample_warehouse(client, admin):
    """Create a warehouse and return its data."""
    response = client.post(
        '/warehouses',
        json={
            'name': 'Test Warehouse',
            'location': 'Lagos',
            'capacity': 1000,
        },
        headers=admin['headers'],
    )
    return response.get_json()['data']
