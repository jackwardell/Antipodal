import os
from functools import wraps

import ipinfo
from flask import request
from geojson import Feature
from geojson import LineString
from geojson import Point
from mapbox import Geocoder

from .models import AntipodeCoefficientCalculation
from .models import db
from .models import Feedback
from .models import PageHit

MAPBOX_API_ACCESS_TOKEN = os.getenv("MAPBOX_API_ACCESS_TOKEN")
IPINFO_API_ACCESS_TOKEN = os.getenv("IPINFO_API_ACCESS_TOKEN")

mapbox_geocoder = Geocoder(access_token=MAPBOX_API_ACCESS_TOKEN)

ipinfo_handler = ipinfo.getHandler(access_token=IPINFO_API_ACCESS_TOKEN)

location_types = [
    "country",
    "region",
    "district",
    "locality",
    "place",
    "neighborhood",
    "poi",
]


def sign(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


def get_ip_address():
    return request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])


def gen_linestring_feature(location_a, location_b):
    """used to gen a geojson linestring"""
    linestring = LineString([location_a.to_geojson(), location_b.to_geojson()])
    return Feature(geometry=linestring)


class Location:
    """
    used to encapsulate all required data for locations in this tool

    a location is a place with a lat and long coord, and potentially a name
    can be used to transfer into geojson with extra properties.

    """

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
                "longitude must be a float or must be able to be cast into a float"
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


def page_hit(fn):
    """decorator to record values to page hit table"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        db.session.add(
            PageHit(
                ip_address=get_ip_address(),
                url=request.path,
            )
        )
        db.session.commit()
        return fn(*args, **kwargs)

    return wrapper


def record_calculation(
    *,
    location_a: Location,
    location_b: Location,
    is_namesake: bool,
    antipode_coefficient: float,
):
    """adapter func to record data to db"""
    calculation = AntipodeCoefficientCalculation(
        ip_address=get_ip_address(),
        is_namesake=is_namesake,
        name_a=location_a.name,
        latitude_a=location_a.latitude,
        longitude_a=location_a.longitude,
        name_b=location_b.name,
        latitude_b=location_b.latitude,
        longitude_b=location_b.longitude,
        antipode_coefficient=antipode_coefficient,
    )
    db.session.add(calculation)
    db.session.commit()


def record_feedback(*, name, email_address, instagram_handle, twitter_handle, feedback):
    """adapter func to record feedback to db"""
    feedback_record = Feedback(
        ip_address=get_ip_address(),
        name=name,
        email_address=email_address,
        instagram_handle=instagram_handle,
        twitter_handle=twitter_handle,
        feedback=feedback,
    )
    db.session.add(feedback_record)
    db.session.commit()
