from flask import abort, Response
from flask import Blueprint
from flask import jsonify
from flask import request
from geojson import FeatureCollection
from geopy.distance import distance

from .models import AntipodeCoefficientCalculation
from .models import Feedback
from .utils import get_features
from .utils import Location
from .utils import record_calculation

# from .models import PageHit

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/location")
def location() -> Response:
    """endpoint for autocompleting location search"""
    location_name = request.args.get("q")

    if not location_name:
        abort(400)

    else:
        features = get_features(location_name)
        return jsonify(
            [
                {"text": i["place_name"], "value": i["geometry"]["coordinates"]}
                for i in features
            ]
        )


@api.route("/calculate")
def calculate() -> Response:
    """endpoint to calculate antipode coefficient"""
    coordinates_a = request.args.get("location_a_coordinates")
    coordinates_b = request.args.get("location_b_coordinates")

    name_a = request.args.get("location_a_name")
    name_b = request.args.get("location_b_name")

    is_namesake = request.args.get("is_namesake") == "true"

    if not all((coordinates_a, coordinates_b, name_a, name_b)):
        abort(400)
    else:
        a = Location.from_mapbox(coordinates_a, name=name_a)
        b = Location.from_mapbox(coordinates_b, name=name_b)
        a_antipode = a.antipode()

        # add class properties for the js to read to assign icons
        a.properties["class"] = "a"
        b.properties["class"] = "b"
        a_antipode.properties["class"] = "antipode-a"

        # calculate antipode coefficient
        a_to_b_distance = distance(a.coordinates, b.coordinates)
        a_to_anti_a_distance = distance(a.coordinates, a.antipode_coordinates)
        antipode_coefficient = a_to_b_distance / a_to_anti_a_distance

        # record calculation to db
        record_calculation(
            location_a=a,
            location_b=b,
            is_namesake=is_namesake,
            antipode_coefficient=antipode_coefficient,
        )

        return jsonify(
            {
                "antipode coefficient": round(antipode_coefficient, 4),
                "geojson": FeatureCollection(
                    [a.to_feature(), b.to_feature(), a_antipode.to_feature()]
                ),
            }
        )


@api.route("/antipode-coefficient-calculations")
def antipode_coefficient_calculations() -> Response:
    _fields = request.args.get("fields")
    fields = _fields.split(",") if (_fields and _fields != "all") else "all"
    shorten = request.args.get("shorten") == "true"

    return jsonify(
        data=[
            i.to_dict(fields=fields, shorten=shorten)
            for i in AntipodeCoefficientCalculation.query.all()
        ]
    )


@api.route("/feedback")
def feedback() -> Response:
    _fields = request.args.get("fields")
    fields = _fields.split(",") if (_fields and _fields != "all") else "all"
    return jsonify(data=[i.to_dict(fields=fields) for i in Feedback.query.all()])


# @api.route("/page-hits")
# def page_hit():
#     return jsonify([i.to_dict() for i in PageHit.query.all()])

# @api.route("/page-hits/ip-addresses")
# def page_hits_ip_addresses():
#     all_page_hits = [i.to_dict() for i in PageHit.query.all()]
#     coords = [
#         [
#             float(j)
#             for j in ipinfo_handler.getDetails(i["ip_address"])
#             .details["loc"]
#             .split(",")[::-1]
#         ]
#         for i in all_page_hits
#     ]
#     return jsonify(coords)
