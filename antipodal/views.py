from flask import Blueprint
from flask import render_template
from flask import request
from geopy.distance import distance

from .utils import Config
from .utils import Location

view = Blueprint("views", __name__)


@view.route("/")
def hello_world():
    print(request.args)
    location_a = request.args.get("location_a")
    location_b = request.args.get("location_b")
    if location_a and location_b:
        a = Location.from_mapbox(location_a)
        b = Location.from_mapbox(location_b)
        a_to_b_distance = distance(a.coordinates, b.coordinates)
        anti_a_to_b_distance = distance(a.antipode_coordinates, b.coordinates)
        antipode_factor = 1 - (
            anti_a_to_b_distance / (anti_a_to_b_distance + a_to_b_distance)
        )

    return render_template("index.html", config=Config)
