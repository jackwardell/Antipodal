import os

from flask import Flask
from geojson import Feature
from geojson import LineString
from geojson import Point
from mapbox import Geocoder

app = Flask(__name__)

MAPBOX_API_ACCESS_TOKEN = os.getenv("MAPBOX_API_ACCESS_TOKEN")

mapbox_geocoder = Geocoder(access_token=MAPBOX_API_ACCESS_TOKEN)
location_types = [
    "country",
    "region",
    "district",
    "locality",
    "place",
    "neighborhood",
    "poi",
]

sign = lambda x: -1 if x < 0 else (1 if x > 0 else 0)


class Config:
    name = "Antipodal Coefficient Calculator"


def gen_linestring_feature(location_a, location_b):
    linestring = LineString([location_a.to_geojson(), location_b.to_geojson()])
    return Feature(geometry=linestring)


class Location:
    def __init__(self, latitude, longitude, name=None):
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
        opposite_longitude_sign = sign(self.longitude) * -1
        self.anti_longitude = (180 - abs(self.longitude)) * opposite_longitude_sign

        self.name = name

        self.properties = {"title": self.name}

    def with_name(self, name):
        self.name = name
        return self

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

    def to_feature(self):
        return Feature(geometry=self.to_point(), properties=self.properties)

    def antipode(self):
        return self.__class__(
            self.anti_latitude, self.anti_longitude, f"Antipode of {self.name}"
        )

    @classmethod
    def from_mapbox(cls, mapbox_coordinates, name=None):
        long, lat = (float(i) for i in mapbox_coordinates.split(","))
        return cls(lat, long, name=name)

    def __repr__(self):
        return f"Location(latitude={self.latitude}, longitude={self.longitude})"

    def __str__(self):
        return f"({self.latitude}, {self.longitude})"
