from flask import Flask, render_template, request, jsonify
import os
from mapbox import Geocoder
from geopy.distance import distance

app = Flask(__name__)

MAPBOX_API_ACCESS_TOKEN = os.getenv("MAPBOX_API_ACCESS_TOKEN")

mapbox_geocoder = Geocoder(access_token=MAPBOX_API_ACCESS_TOKEN)
location_types = ["country", "region", "district", "locality", "place", "neighborhood"]


class Config:
    name = "Antipodal Coefficient Calculator"


class Location:

    def __init__(self, latitude, longitude):
        assert isinstance(latitude, float), "latitude must be a float"
        assert -90 <= latitude <= 90, "latitude must be between -90 and 90 degrees"
        self.latitude = latitude

        assert isinstance(longitude, float), "longitude must be a float"
        assert -180 <= longitude <= 180, "longitude must be between -90 and 90 degrees"
        self.longitude = longitude

    @property
    def coordinates(self):
        return self.latitude, self.longitude

    @property
    def antipode_coordinates(self):
        return -self.latitude, 180 - self.longitude

    @classmethod
    def from_mapbox(cls, mapbox_coordinates):
        long, lat = (float(i) for i in mapbox_coordinates.split(","))
        return cls(lat, long)

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude})"

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"


@app.route("/")
def hello_world():
    print(request.args)
    location_a = request.args.get("location_a")
    location_b = request.args.get("location_b")
    if location_a and location_b:
        a = Location.from_mapbox(location_a)
        b = Location.from_mapbox(location_b)
        a_to_b_distance = distance(a.coordinates, b.coordinates)
        anti_a_to_b_distance = distance(a.antipode_coordinates, b.coordinates)
        antipode_factor = 1 - (anti_a_to_b_distance / (anti_a_to_b_distance + a_to_b_distance))

    return render_template("index.html", config=Config)


@app.route("/result")
def results():
    return render_template('result.html')


@app.route("/api/location")
def search_dropdown():
    location = request.args.get("q")
    query = mapbox_geocoder.forward(location, types=location_types)
    results = query.json()["features"]
    return jsonify(
        [
            {"text": i["place_name"], "value": i["geometry"]["coordinates"]}
            for i in results
        ]
    )
    # return jsonify([i["place_name"] for i in results])


# @app.route('/api/geojson')

if __name__ == "__main__":
    app.run()
