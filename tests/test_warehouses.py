"""
Warehouse assignment tests.
"""

def test_assign_shipment_to_warehouse(client, customer, admin, sample_shipment, sample_warehouse):
    shipment_id = sample_shipment['id']
    warehouse_id = sample_warehouse['id']

    response = client.put(
        f'/shipments/{shipment_id}/assign-warehouse',
        json={'warehouse_id': warehouse_id},
        headers=customer['headers'],
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert body['data']['warehouse_id'] == warehouse_id


def test_assign_shipment_to_missing_warehouse(client, customer, sample_shipment):
    response = client.put(
        f'/shipments/{sample_shipment["id"]}/assign-warehouse',
        json={'warehouse_id': 9999},
        headers=customer['headers'],
    )

    assert response.status_code == 404
    assert response.get_json()['success'] is False
