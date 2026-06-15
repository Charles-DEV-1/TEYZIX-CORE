"""
Delivery agent assignment tests.
"""

def test_assign_agent_to_shipment(client, admin, agent, sample_shipment):
    shipment_id = sample_shipment['id']
    agent_id = agent['user_id']

    response = client.put(
        f'/shipments/{shipment_id}/assign-agent',
        json={'agent_id': agent_id},
        headers=admin['headers'],
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body['success'] is True
    assert body['data']['agent_id'] == agent_id


def test_assign_agent_requires_admin(client, customer, agent, sample_shipment):
    response = client.put(
        f'/shipments/{sample_shipment["id"]}/assign-agent',
        json={'agent_id': agent['user_id']},
        headers=customer['headers'],
    )

    assert response.status_code == 403
    assert response.get_json()['success'] is False
