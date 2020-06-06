import json

from flask.helpers import url_quote

# location data
location_a_name = "Camberwell Green, London, Greater London, England, United Kingdom"
longitude_a = 145.071
latitude_a = -37.835
location_a_coords = f"{longitude_a},{latitude_a}"

location_b_name = "Camberwell, Victoria, Australia"
longitude_b = -0.0938
latitude_b = 51.4739
location_b_coords = f"{longitude_b},{latitude_b}"

anti_a_coords = [-34.929, 37.835]


def test_location_api(test_client):
    response = test_client.get("/api/location")
    assert response.status_code == 400


def test_calculate_api(test_client):
    response = test_client.get("/api/calculate")
    assert response.status_code == 400

    # incorrect queries
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

    # correct query
    response = test_client.get(
        "/api/calculate"
        f"?location_a_coordinates={url_quote(location_a_coords)}"
        f"&location_b_coordinates={url_quote(location_a_coords)}"
        f"&location_a_name={url_quote(location_a_name)}"
        f"&location_b_name={url_quote(location_b_name)}"
    )
    assert response.status_code == 200

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
    assert "features" in data["geojson"]
    assert isinstance(data["geojson"]["features"], list)

    features = data["geojson"]["features"]
    assert len(features) == 3
    assert {
        "geometry": {
            "coordinates": [float(i) for i in location_a_coords.split(",")],
            "type": "Point",
        },
        "properties": {"class": "a", "title": location_a_name},
        "type": "Feature",
    } in features

    assert {
        "geometry": {
            "coordinates": [float(i) for i in location_b_coords.split(",")],
            "type": "Point",
        },
        "properties": {"class": "b", "title": location_b_name},
        "type": "Feature",
    } in features

    assert {
        "geometry": {"coordinates": anti_a_coords, "type": "Point"},
        "properties": {
            "class": "antipode-a",
            "title": f"Antipode of {location_a_name}",
        },
        "type": "Feature",
    } in features


def test_page_hits_api(test_client):
    # hit index
    test_client.get("/")

    # testing api
    response = test_client.get("/api/page-hits")
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert data
    assert isinstance(data, list)
    assert len(data) == 1
    assert isinstance(data[0], dict)
    assert data[0]["id"] == 1
    assert data[0]["ip_address"] == "127.0.0.1"
    assert data[0]["url"] == "/"


def test_antipode_coefficient_calculations_api(test_client):
    response = test_client.get("/api/antipode-coefficient-calculations")
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert data
    assert isinstance(data, list)
    assert len(data) == 1

    calc = data[0]
    assert len(calc) == 11
    assert isinstance(calc, dict)
    assert calc["id"] == 1
    assert calc["ip_address"] == "127.0.0.1"

    # a
    assert calc["name_a"] == location_a_name
    assert calc["latitude_a"] == latitude_a
    assert calc["longitude_a"] == longitude_a

    # b
    assert calc["name_b"] == location_b_name
    assert calc["latitude_b"] == latitude_b
    assert calc["longitude_b"] == longitude_b

    assert calc["is_namesake"] == True
    assert calc["antipode_coefficient"] == 0.8451353577287053
