from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import sql

db = SQLAlchemy()


class PageHit(db.Model):

    __tablename__ = "page_hit"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
    timestamp = db.Column(db.DateTime, server_default=sql.func.now(), index=True)
    ip_address = db.Column(db.String)
    url = db.Column(db.String, nullable=False)

    def hit_date(self):
        return self.timestamp.strftime("%d %b %Y")


# class AntipodeCoefficientCalculation:
#
#     __tablename__ = "antipode_coefficient_calculation"
#
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True, index=True)
#     timestamp = db.Column(db.DateTime, server_default=sql.func.now(), index=True)
#     ip_address = db.Column(db.String)
#
#     name_a = db.Column(db.String)
#     latitude_a = db.Column(db.Float)
#     longitude_b = db.Column(db.Float)
#
#     name_b = db.Column(db.String)
#     latitude_a = db.Column(db.Float)
#     longitude_b = db.Column(db.Float)
