from flask import Blueprint
from flask import abort
from flask import jsonify
from flask import request
from geojson import FeatureCollection
from geopy.distance import distance

from .utils import Location
from .utils import location_types
from .utils import mapbox_geocoder
from .utils import record_calculation
from .models import PageHit
from .models import AntipodeCoefficientCalculation

api = Blueprint("api", __name__, url_prefix="/api")


@api.route("/location")
def location():
    """endpoint for autocompleting location search"""
    location_name = request.args.get("q")

    if not location_name:
        abort(400)

    else:
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


@api.route("/page-hits")
def page_hits():
    return jsonify([i.to_dict() for i in PageHit.query.all()])


@api.route("/antipode-coefficient-calculations")
def antipode_coefficient_calculations():
    _fields = request.args.get("fields")
    fields = _fields.split(",") if (_fields and _fields != "all") else "all"
    for_table = request.args.get("for_table") == "true"
    shorten = request.args.get("shorten") == "true"

    if for_table:
        return jsonify(
            {
                "data": [
                    list(i.to_dict(fields=fields, shorten=shorten).values())
                    for i in AntipodeCoefficientCalculation.query.all()
                ]
            }
        )
    elif not for_table:
        return jsonify(
            [
                i.to_dict(fields=fields, shorten=shorten)
                for i in AntipodeCoefficientCalculation.query.all()
            ]
        )
    else:
        abort(400)
