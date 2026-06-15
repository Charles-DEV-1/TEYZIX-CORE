"""
Reports endpoint tests.
"""

def test_daily_shipments_report(client, admin, sample_shipment):
    response = client.get('/reports/daily-shipments', headers=admin['headers'])

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert body['data']['total_shipments'] >= 1
    assert 'delivered_shipments' in body['data']
    assert 'pending_shipments' in body['data']


def test_delivered_report(client, admin):
    response = client.get('/reports/delivered', headers=admin['headers'])

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert 'total_shipments' in body['data']
    assert 'shipments' in body['data']


def test_pending_report(client, admin, sample_shipment):
    response = client.get('/reports/pending', headers=admin['headers'])

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert body['data']['pending_shipments'] >= 1


def test_warehouse_utilization_report(client, admin, sample_warehouse):
    response = client.get('/reports/warehouse-utilization', headers=admin['headers'])

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert 'overall_utilization_percentage' in body['data']
    assert len(body['data']['warehouses']) >= 1


def test_reports_require_admin(client, customer):
    response = client.get('/reports/daily-shipments', headers=customer['headers'])

    assert response.status_code == 403
    assert response.get_json()['success'] is False
