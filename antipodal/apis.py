from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from .utils import Location
from .utils import location_types
from .utils import mapbox_geocoder
from .utils import gen_linestring_feature

from geojson import FeatureCollection

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


@api.route("/geojson")
def geojson_point():
    latitude_a = request.args.get("latitude_a")
    longitude_a = request.args.get("longitude_a")
    title_a = request.args.get("title_a")

    latitude_b = request.args.get("latitude_b")
    longitude_b = request.args.get("longitude_b")
    title_b = request.args.get("title_b")

    if not latitude_a and longitude_a and latitude_b and longitude_b:
        abort(404)
    else:
        location_a = Location(latitude_a, longitude_a, title_a)
        location_b = Location(latitude_b, longitude_b, title_b)

        return jsonify(
            FeatureCollection(
                [
                    location_a.to_feature(id_="a"),
                    location_b.to_feature(id_="b"),
                    location_a.antipode().to_feature(id_="anti_a"),
                    gen_linestring_feature(location_a, location_b, "ab"),
                    gen_linestring_feature(
                        location_b, location_a.antipode(), "b_anti_a"
                    ),
                ]
            )
        )
