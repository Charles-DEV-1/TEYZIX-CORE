"""
Authentication endpoint tests.
"""

from tests.conftest import register_user, login_user


def test_register_success(client):
    response = register_user(client, 'Jane Doe', 'jane@test.com')

    assert response.status_code == 201
    body = response.get_json()
    assert body['success'] is True
    assert body['data']['user']['email'] == 'jane@test.com'
    assert body['data']['user']['role'] == 'customer'


def test_register_duplicate_email(client):
    register_user(client, 'Jane Doe', 'jane@test.com')
    response = register_user(client, 'Jane Again', 'jane@test.com')

    assert response.status_code == 400
    assert response.get_json()['success'] is False


def test_login_success(client):
    register_user(client, 'Jane Doe', 'jane@test.com')
    response = login_user(client, 'jane@test.com')

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert 'access_token' in body['data']
    assert 'refresh_token' in body['data']


def test_login_invalid_password(client):
    register_user(client, 'Jane Doe', 'jane@test.com')
    response = client.post(
        '/auth/login',
        json={'email': 'jane@test.com', 'password': 'WrongPass1!'},
    )

    assert response.status_code == 401
    assert response.get_json()['success'] is False


def test_refresh_token(client, customer):
    response = client.post('/auth/refresh', headers=customer['refresh_headers'])

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert 'access_token' in body['data']


def test_refresh_requires_refresh_token(client, customer):
    response = client.post('/auth/refresh', headers=customer['headers'])

    assert response.status_code == 422
