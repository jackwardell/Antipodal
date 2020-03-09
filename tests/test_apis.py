import json


def test_location_api(test_client):
    response = test_client.get("/api/location")
    assert response.status_code == 400


def test_calculate_api(test_client):
    response = test_client.get("/api/calculate")
    assert response.status_code == 400

    # incorrect queries
    response = test_client.get(
        "/api/calculate"
        # "?location_a_coordinates=-0.0938%2C51.4739"
        "?location_b_coordinates=145.071%2C-37.835"
        "&location_a_name=Camberwell%20Green%2C%20London%2C%20Greater%20London%2C%20England%2C%20United%20Kingdom"
        "&location_b_name=Camberwell%2C%20Victoria%2C%20Australia"
        "&is_namesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        "?location_a_coordinates=-0.0938%2C51.4739"
        # "&location_b_coordinates=145.071%2C-37.835"
        "&location_a_name=Camberwell%20Green%2C%20London%2C%20Greater%20London%2C%20England%2C%20United%20Kingdom"
        "&location_b_name=Camberwell%2C%20Victoria%2C%20Australia"
        "&is_namesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        "?location_a_coordinates=-0.0938%2C51.4739"
        "&location_b_coordinates=145.071%2C-37.835"
        # "&location_a_name=Camberwell%20Green%2C%20London%2C%20Greater%20London%2C%20England%2C%20United%20Kingdom"
        "&location_b_name=Camberwell%2C%20Victoria%2C%20Australia"
        "&is_namesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        "?location_a_coordinates=-0.0938%2C51.4739"
        "&location_b_coordinates=145.071%2C-37.835"
        "&location_a_name=Camberwell%20Green%2C%20London%2C%20Greater%20London%2C%20England%2C%20United%20Kingdom"
        # "&location_b_name=Camberwell%2C%20Victoria%2C%20Australia"
        "&is_namesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        "?location_a_coordinates=-0.0938%2C51.4739"
        "&location_b_coordinates=145.071%2C-37.835"
        "&location_a_name=Camberwell%20Green%2C%20London%2C%20Greater%20London%2C%20England%2C%20United%20Kingdom"
        "&location_b_name=Camberwell%2C%20Victoria%2C%20Australia"
        # "&is_namesake=true"
    )
    assert response.status_code == 400

    # correct query
    response = test_client.get(
        "/api/calculate"
        "?location_a_coordinates=-0.0938%2C51.4739"
        "&location_b_coordinates=145.071%2C-37.835"
        "&location_a_name=Camberwell%20Green%2C%20London%2C%20Greater%20London%2C%20England%2C%20United%20Kingdom"
        "&location_b_name=Camberwell%2C%20Victoria%2C%20Australia"
        "&is_namesake=true"
    )
    assert response.status_code == 200


def test_page_hits_api(test_client):
    response = test_client.get("/api/page-hits")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data
    assert isinstance(data, list)
    print(data)


def test_antipode_coefficient_calculations_api(test_client):
    response = test_client.get("/api/antipode-coefficient-calculations")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert data
    assert isinstance(data, list)
    print(data)
