import json
from flask.helpers import url_quote


def test_location_api(test_client):
    response = test_client.get("/api/location")
    assert response.status_code == 400


def test_calculate_api(test_client):
    response = test_client.get("/api/calculate")
    assert response.status_code == 400

    # incorrect queries
    location_a_name = "Camberwell Green, London, Greater London, England, United Kingdom"
    location_a_coords = "145.071,-37.835"
    location_b_name = "Camberwell, Victoria, Australia"
    location_b_coords = "-0.0938,51.4739"

    response = test_client.get(
        "/api/calculate"
        f"?location_b_coordinates={url_quote(location_b_coords)}"
        f"&location_a_name={url_quote(location_a_name)}"
        f"&location_b_name={url_quote(location_b_name)}"
        "&is_namesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        f"?location_a_coordinates={url_quote(location_a_coords)}"
        f"&location_a_name={url_quote(location_a_name)}"
        f"&location_b_name={url_quote(location_b_name)}"
        "&is_namesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        f"?location_a_coordinates={url_quote(location_a_name)}"
        f"&location_b_coordinates={url_quote(location_b_coords)}"
        f"&location_b_name={url_quote(location_b_name)}"
        "&is_nafmesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        f"?location_a_coordinates={url_quote(location_a_coords)}"
        f"&location_b_coordinates={url_quote(location_b_coords)}"
        f"&location_a_name={url_quote(location_a_name)}"
        "&is_namesake=true"
    )
    assert response.status_code == 400
    response = test_client.get(
        "/api/calculate"
        f"?location_a_coordinates={url_quote(location_a_coords)}"
        f"&location_b_coordinates={url_quote(location_a_coords)}"
        f"&location_a_name={url_quote(location_a_name)}"
        f"&location_b_name={url_quote(location_b_name)}"
    )
    assert response.status_code == 400

    # correct query
    response = test_client.get(
        "/api/calculate"
        f"?location_a_coordinates={url_quote(location_a_coords)}"
        f"&location_b_coordinates={url_quote(location_b_coords)}"
        f"&location_a_name={url_quote(location_a_name)}"
        f"&location_b_name={url_quote(location_b_name)}"
        "&is_namesake=true"
    )
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert data
    assert isinstance(data, dict)

    assert "antipode coefficient" in data
    assert data["antipode coefficient"] == 0.8451

    assert "geojson" in data
    assert isinstance(data["geojson"], dict)
    assert "type" in data["geojson"]
    assert data["geojson"]["type"] == "FeatureCollection"
    # assert data["geojson"] == {
    #     "features": [
    #         {
    #             "geometry": {"coordinates": [-0.0938, 51.4739], "type": "Point"},
    #             "properties": {
    #                 "class": "a",
    #                 "title": "Camberwell Green, London, Greater London, England, United Kingdom",
    #             },
    #             "type": "Feature",
    #         },
    #         {
    #             "geometry": {"coordinates": [145.071, -37.835], "type": "Point"},
    #             "properties": {
    #                 "class": "b",
    #                 "title": "Camberwell, Victoria, Australia",
    #             },
    #             "type": "Feature",
    #         },
    #         {
    #             "geometry": {"coordinates": [179.9062, -51.4739], "type": "Point"},
    #             "properties": {
    #                 "class": "antipode-a",
    #                 "title": "Antipode of Camberwell Green, London, Greater London, England, United Kingdom",
    #             },
    #             "type": "Feature",
    #         },
    #     ],
    #     "type": "FeatureCollection",
    # }


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
