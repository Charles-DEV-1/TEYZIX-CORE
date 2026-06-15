"""
Shipment endpoint tests.
"""


def test_create_shipment(client, customer):
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

    assert response.status_code == 201
    body = response.get_json()
    assert body['success'] is True
    assert body['data']['status'] == 'CREATED'
    assert body['data']['tracking_id'].startswith('SHP')


def test_create_shipment_requires_auth(client):
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
    )

    assert response.status_code == 401


def test_track_shipment(client, customer, sample_shipment):
    tracking_id = sample_shipment['tracking_id']
    response = client.get(
        f'/shipments/track/{tracking_id}',
        headers=customer['headers'],
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert body['data']['tracking_id'] == tracking_id
    assert 'tracking_history' in body['data']
