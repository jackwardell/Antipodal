import json
from unittest.mock import patch

import pytest
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

mapbox_return_value = [
    {
        "id": "locality.4681727490391160",
        "type": "Feature",
        "place_type": ["locality"],
        "relevance": 1,
        "properties": {"wikidata": "Q2934668"},
        "text": "Camberwell",
        "place_name": "Camberwell, Victoria, Australia",
        "bbox": [145.0531367, -37.85082702, 145.09815449, -37.82044789],
        "center": [145.071, -37.835],
        "geometry": {"type": "Point", "coordinates": [145.071, -37.835]},
        "context": [
            {
                "id": "place.7068896531111320",
                "wikidata": "Q3141",
                "text": "Melbourne",
            },
            {
                "id": "region.10151275538899450",
                "wikidata": "Q36687",
                "short_code": "AU-VIC",
                "text": "Victoria",
            },
            {
                "id": "country.9968792518346070",
                "wikidata": "Q408",
                "short_code": "au",
                "text": "Australia",
            },
        ],
    },
    {
        "id": "locality.11041229601730240",
        "type": "Feature",
        "place_type": ["locality"],
        "relevance": 1,
        "properties": {"wikidata": "Q385060"},
        "text": "Camberwell Green",
        "place_name": "Camberwell Green, London, Greater London, England, United Kingdom",
        "bbox": [
            -0.105554331526632,
            51.4698808879779,
            -0.085799805698378,
            51.4837524249822,
        ],
        "center": [-0.0938, 51.4739],
        "geometry": {"type": "Point", "coordinates": [-0.0938, 51.4739]},
        "context": [
            {
                "id": "place.8780954591631530",
                "wikidata": "Q84",
                "text": "London",
            },
            {
                "id": "district.14664713661976620",
                "wikidata": "Q23306",
                "text": "Greater London",
            },
            {
                "id": "region.13483278848453920",
                "wikidata": "Q21",
                "short_code": "GB-ENG",
                "text": "England",
            },
            {
                "id": "country.12405201072814600",
                "wikidata": "Q145",
                "short_code": "gb",
                "text": "United Kingdom",
            },
        ],
    },
    {
        "id": "poi.790274063969",
        "type": "Feature",
        "place_type": ["poi"],
        "relevance": 1,
        "properties": {
            "wikidata": "Q2934669",
            "category": "college, university",
            "landmark": True,
            "address": "Peckham Rd.",
            "foursquare": "4b7bdb80f964a520e6702fe3",
            "maki": "college",
        },
        "text": "Camberwell College of Arts",
        "place_name": "Camberwell College of Arts, Peckham Rd., London, England SE5 8UF, United Kingdom",
        "center": [-0.0804375, 51.474083500000006],
        "geometry": {
            "coordinates": [-0.0804375, 51.474083500000006],
            "type": "Point",
        },
        "context": [
            {"id": "postcode.15994448477025910", "text": "SE5 8UF"},
            {"id": "locality.7228919090953860", "text": "Brunswick Park"},
            {
                "id": "place.8780954591631530",
                "wikidata": "Q84",
                "text": "London",
            },
            {
                "id": "district.14664713661976620",
                "wikidata": "Q23306",
                "text": "Greater London",
            },
            {
                "id": "region.13483278848453920",
                "wikidata": "Q21",
                "short_code": "GB-ENG",
                "text": "England",
            },
            {
                "id": "country.12405201072814600",
                "wikidata": "Q145",
                "short_code": "gb",
                "text": "United Kingdom",
            },
        ],
    },
    {
        "id": "poi.661425025962",
        "type": "Feature",
        "place_type": ["poi"],
        "relevance": 1,
        "properties": {
            "foursquare": "4b3990e8f964a520c15d25e3",
            "landmark": True,
            "address": "Market Pl.",
            "category": "farmers market, farmers, market",
        },
        "text": "Camberwell Market",
        "place_name": "Camberwell Market, Market Pl., Melbourne, Victoria 3124, Australia",
        "center": [145.057898, -37.829955],
        "geometry": {
            "coordinates": [145.057898, -37.829955],
            "type": "Point",
        },
        "context": [
            {"id": "postcode.10346171276522500", "text": "3124"},
            {
                "id": "locality.4681727490391160",
                "wikidata": "Q2934668",
                "text": "Camberwell",
            },
            {
                "id": "place.7068896531111320",
                "wikidata": "Q3141",
                "text": "Melbourne",
            },
            {
                "id": "region.10151275538899450",
                "wikidata": "Q36687",
                "short_code": "AU-VIC",
                "text": "Victoria",
            },
            {
                "id": "country.9968792518346070",
                "wikidata": "Q408",
                "short_code": "au",
                "text": "Australia",
            },
        ],
    },
    {
        "id": "poi.171798708638",
        "type": "Feature",
        "place_type": ["poi"],
        "relevance": 1,
        "properties": {
            "foursquare": "4bdfdbbce75c0f47c57bcc03",
            "landmark": True,
            "address": "793 Burke Road",
            "category": "mall, shop",
        },
        "text": "Camberwell Place",
        "place_name": "Camberwell Place, 793 Burke Road, Melbourne, Victoria 3124, Australia",
        "center": [145.056852, -37.829125],
        "geometry": {
            "coordinates": [145.056852, -37.829125],
            "type": "Point",
        },
        "context": [
            {"id": "postcode.10346171276522500", "text": "3124"},
            {
                "id": "locality.4681727490391160",
                "wikidata": "Q2934668",
                "text": "Camberwell",
            },
            {
                "id": "place.7068896531111320",
                "wikidata": "Q3141",
                "text": "Melbourne",
            },
            {
                "id": "region.10151275538899450",
                "wikidata": "Q36687",
                "short_code": "AU-VIC",
                "text": "Victoria",
            },
            {
                "id": "country.9968792518346070",
                "wikidata": "Q408",
                "short_code": "au",
                "text": "Australia",
            },
        ],
    },
]


@pytest.fixture
def mock_forward() -> None:
    with patch("antipodal.utils.get_features", return_value=mapbox_return_value):
        yield


def test_location_api(mock_forward, test_client) -> None:
    antipode_return_value = [
        {"text": "Camberwell, Victoria, Australia", "value": [145.071, -37.835]},
        {
            "text": "Camberwell Green, London, Greater London, England, United Kingdom",
            "value": [-0.0938, 51.4739],
        },
        {
            "text": "Camberwell College of Arts, Peckham Rd., London, England SE5 8UF, United Kingdom",
            "value": [-0.0804375, 51.474083500000006],
        },
        {
            "text": "Camberwell Market, Market Pl., Melbourne, Victoria 3124, Australia",
            "value": [145.057898, -37.829955],
        },
        {
            "text": "Camberwell Place, 793 Burke Road, Melbourne, Victoria 3124, Australia",
            "value": [145.056852, -37.829125],
        },
    ]

    response = test_client.get("/api/location")
    assert response.status_code == 400

    response = test_client.get("/api/location?q=camberwell")
    assert response.json == antipode_return_value


def test_calculate_api(test_client) -> None:
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


# def test_page_hits_api(test_client):
#     # hit index
#     test_client.get("/")
#
#     # testing api
#     response = test_client.get("/api/page-hits")
#     assert response.status_code == 200
#
#     data = json.loads(response.data.decode())
#     assert data
#     assert isinstance(data, list)
#     assert len(data) == 1
#     assert isinstance(data[0], dict)
#     assert data[0]["id"] == 1
#     assert data[0]["ip_address"] == "127.0.0.1"
#     assert data[0]["url"] == "/"


def test_antipode_coefficient_calculations_api(test_client) -> None:
    # correct query
    response = test_client.get(
        "/api/calculate"
        f"?location_a_coordinates={url_quote(location_a_coords)}"
        f"&location_b_coordinates={url_quote(location_b_coords)}"
        f"&location_a_name={url_quote(location_a_name)}"
        f"&location_b_name={url_quote(location_b_name)}"
    )
    assert response.status_code == 200

    response = test_client.get("/api/antipode-coefficient-calculations")
    assert response.status_code == 200

    resp_json = response.json
    assert isinstance(resp_json, dict)

    data = resp_json["data"]
    assert len(data) == 1

    calc = data[0]
    assert len(calc) == 10
    assert isinstance(calc, dict)
    assert calc["id"] == 1

    # a
    assert calc["name_a"] == location_a_name
    assert calc["latitude_a"] == latitude_a
    assert calc["longitude_a"] == longitude_a

    # b
    assert calc["name_b"] == location_b_name
    assert calc["latitude_b"] == latitude_b
    assert calc["longitude_b"] == longitude_b

    assert calc["is_namesake"] is False
    assert calc["antipode_coefficient"] == 0.8451353577287053
