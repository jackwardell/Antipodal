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


class AntipodeCoefficientCalculation(db.Model):
    __tablename__ = "antipode_coefficient_calculation"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    timestamp = db.Column(db.DateTime, server_default=sql.func.now(), nullable=False, index=True)
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
        return self.timestamp.strftime("%H:%M:%S %Y-%m-%d")
