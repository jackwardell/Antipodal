def test_home_view(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Wardell's Antipode Namesake Coefficient" in response.data


def test_results_view(test_client):
    response = test_client.get('/results')
    assert response.status_code == 200
    assert b"Wardell's Antipode Namesake Coefficient" in response.data
