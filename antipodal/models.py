from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql

db = SQLAlchemy()


class PageHit(db.Model):
    __tablename__ = "page_hit"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    timestamp = db.Column(db.DateTime, server_default=sql.func.now(), index=True)
    ip_address = db.Column(db.String)
    url = db.Column(db.String, nullable=False)

    @property
    def hit_date(self):
        return self.timestamp.strftime("%d %b %Y")

    def to_dict(self):
        data = {
            "id": self.id,
            "timestamp": self.timestamp,
            "ip_address": self.ip_address,
            "url": self.url,
        }
        return data


class AntipodeCoefficientCalculation(db.Model):
    __tablename__ = "antipode_coefficient_calculation"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    timestamp = db.Column(
        db.DateTime, server_default=sql.func.now(), nullable=False, index=True
    )
    ip_address = db.Column(db.String)

    name_a = db.Column(db.String, nullable=False, index=True)
    latitude_a = db.Column(db.Float, nullable=False)
    longitude_a = db.Column(db.Float, nullable=False)

    name_b = db.Column(db.String, nullable=False, index=True)
    latitude_b = db.Column(db.Float, nullable=False)
    longitude_b = db.Column(db.Float, nullable=False)

    is_namesake = db.Column(db.Boolean, default=False, nullable=False, index=True)
    antipode_coefficient = db.Column(db.Float, nullable=False, index=True)

    @property
    def calc_time(self):
        return self.timestamp.strftime("%Y-%m-%d")

    def shorten_name(self, attr_name):
        places = getattr(self, attr_name).split(",")
        if len(places) > 3:
            shorter_name = places[0:2] + [places[-1]]
            return ", ".join(shorter_name)
        else:
            return ", ".join(places)

    @property
    def location_a_name(self):
        return self.shorten_name("name_a")

    @property
    def location_b_name(self):
        return self.shorten_name("name_b")

    def to_dict(self, fields="all", shorten=False):
        _data = {
            "id": self.id,
            "timestamp": self.calc_time,
            "ip_address": self.ip_address,
            "name_a": self.name_a if not shorten else self.location_a_name,
            "latitude_a": self.latitude_a,
            "longitude_a": self.longitude_a,
            "name_b": self.name_b if not shorten else self.location_b_name,
            "latitude_b": self.latitude_b,
            "longitude_b": self.longitude_b,
            "is_namesake": self.is_namesake,
            "antipode_coefficient": self.antipode_coefficient
            if not shorten
            else round(self.antipode_coefficient, 4),
        }
        # if fields != "all":
        #     assert isinstance(fields, list)
        # assert fields in
        data = {i: _data[i] for i in fields} if fields != "all" else _data
        return data


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    timestamp = db.Column(
        db.DateTime, server_default=sql.func.now(), nullable=False, index=True
    )
    ip_address = db.Column(db.String)

    name = db.Column(db.String, nullable=False, index=True)

    email_address = db.Column(db.String, nullable=True)
    instagram_handle = db.Column(db.String, nullable=True)
    twitter_handle = db.Column(db.String, nullable=True)

    feedback = db.Column(db.Text, nullable=False)

    @property
    def feedback_date(self):
        return self.timestamp.strftime("%Y-%m-%d")

    def to_dict(self, fields="all"):
        _data = {
            "id": self.id,
            "timestamp": self.feedback_date,
            "ip_address": self.ip_address,
            "name": self.name,
            "feedback": self.feedback,
        }
        data = {i: _data[i] for i in fields} if fields != "all" else _data
        return data
