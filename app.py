from flask import Flask, render_template, request, jsonify, abort
import os
from mapbox import Geocoder
from geopy.distance import distance
from geojson import Point, Feature, LineString, FeatureCollection

app = Flask(__name__)

MAPBOX_API_ACCESS_TOKEN = os.getenv("MAPBOX_API_ACCESS_TOKEN")

mapbox_geocoder = Geocoder(access_token=MAPBOX_API_ACCESS_TOKEN)
location_types = ["country", "region", "district", "locality", "place", "neighborhood"]


class Config:
    name = "Antipodal Coefficient Calculator"


def gen_linestring_feature(location_a, location_b, id_):
    linestring = LineString([location_a.to_geojson(), location_b.to_geojson()])
    return Feature(id=id_, geometry=linestring)


class Location:
    def __init__(self, latitude, longitude, name=None, **kwargs):
        try:
            self.latitude = float(latitude)
        except ValueError:
            raise ValueError(
                "latitude must be must be a float "
                "or must be able to be cast into a float"
            )
        assert (
            -90.0 <= self.latitude <= 90.0
        ), "latitude must be between -90 and 90 degrees"
        self.anti_latitude = -self.latitude

        try:
            self.longitude = float(longitude)
        except ValueError:
            raise ValueError(
                "longitude must be a float " "or must be able to be cast into a float"
            )
        assert (
            -180.0 <= self.longitude <= 180.0
        ), "longitude must be between -90 and 90 degrees"
        self.anti_longitude = 180 - self.longitude

        self.name = name

        self.properties = {"title": self.name}.update(kwargs)

    @property
    def coordinates(self):
        return self.latitude, self.longitude

    @property
    def antipode_coordinates(self):
        return self.anti_latitude, self.anti_longitude

    def to_geojson(self):
        return self.longitude, self.latitude

    def to_point(self):
        return Point(self.to_geojson())

    def to_feature(self, id_):
        return Feature(id=id_, geometry=self.to_point(), properties=self.properties)

    def antipode(self):
        return self.__class__(self.anti_latitude, self.anti_longitude, self.name)

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
        antipode_factor = 1 - (
            anti_a_to_b_distance / (anti_a_to_b_distance + a_to_b_distance)
        )

    return render_template("index.html", config=Config)


@app.route("/result")
def result():
    return render_template("result.html")


@app.route("/api/location")
def search_dropdown():
    location = request.args.get("q")
    query = mapbox_geocoder.forward(location, types=location_types, limit=5)
    results = query.json()["features"]
    return jsonify(
        [
            {"text": i["place_name"], "value": i["geometry"]["coordinates"]}
            for i in results
        ]
    )


@app.route("/api/geojson")
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
                    location_a.to_feature(id_='a'),
                    location_b.to_feature(id_='b'),
                    location_a.antipode().to_feature(id_='anti_a'),
                    gen_linestring_feature(location_a, location_b, 'ab'),
                    gen_linestring_feature(location_b, location_a.antipode(), 'b_anti_a'),
                ]
            )
        )

@app.route('/he')
def he():
    return render_template('index2.html')


if __name__ == "__main__":
    app.run()
