from flask import Blueprint
from flask import render_template

view = Blueprint("views", __name__)


@view.route("/")
def hello_world():
    return render_template("index.html")
