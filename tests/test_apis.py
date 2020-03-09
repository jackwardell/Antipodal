def test_location_api(test_client):
    response = test_client.get('/api/location')
    assert response.status_code == 400


def test_calculate_api(test_client):
    response = test_client.get('/api/calculate')
    assert response.status_code == 400
