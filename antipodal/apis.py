from flask import Blueprint
from flask import abort
from flask import jsonify
from flask import request
from geojson import FeatureCollection
from geopy.distance import distance

from .utils import Location
from .utils import gen_linestring_feature
from .utils import location_types
from .utils import mapbox_geocoder

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/location")
def location():
    location_name = request.args.get("q")
    query = mapbox_geocoder.forward(location_name, types=location_types, limit=5)
    results = query.json()["features"]
    return jsonify(
        [
            {"text": i["place_name"], "value": i["geometry"]["coordinates"]}
            for i in results
        ]
    )


@api.route("/calculate")
def calculate():
    coordinates_a = request.args.get("location_a_coordinates")
    coordinates_b = request.args.get("location_b_coordinates")

    if not coordinates_a and coordinates_b:
        abort(404)
    else:
        a = Location.from_mapbox(coordinates_a)
        b = Location.from_mapbox(coordinates_b)
        a_to_b_distance = distance(a.coordinates, b.coordinates)
        a_to_anti_a_distance = distance(a.coordinates, a.antipode_coordinates)
        antipode_coefficient = a_to_b_distance / a_to_anti_a_distance
        return jsonify({"antipode coefficient": round(antipode_coefficient, 4)})


@api.route("/geojson/point")
def geojson_point():
    coordinates_a = request.args.get("location_a_coordinates")
    coordinates_b = request.args.get("location_b_coordinates")

    name_a = request.args.get("location_a_name")
    name_b = request.args.get("location_b_name")

    if not coordinates_a and coordinates_b:
        abort(404)
    else:
        a = Location.from_mapbox(coordinates_a, name=name_a)
        b = Location.from_mapbox(coordinates_b, name=name_b)
        a_antipode = a.antipode()

        a.properties["class"] = "a"
        b.properties["class"] = "b"
        a_antipode.properties["class"] = "antipode-a"

        return jsonify(
            FeatureCollection(
                [
                    a.to_feature(),
                    b.to_feature(),
                    a_antipode.to_feature(),
                ]
            )
        )


@api.route("/geojson/line")
def geojson_line():
    coordinates_a = request.args.get("location_a_coordinates")
    coordinates_b = request.args.get("location_b_coordinates")

    name_a = request.args.get("location_a_name")
    name_b = request.args.get("location_b_name")

    if not coordinates_a and coordinates_b:
        abort(404)
    else:
        a = Location.from_mapbox(coordinates_a, name=name_a)
        b = Location.from_mapbox(coordinates_b, name=name_b)

        return jsonify(
            FeatureCollection(
                [
                    gen_linestring_feature(a, b),
                    gen_linestring_feature(b, a.antipode())
                ]
            )
        )
