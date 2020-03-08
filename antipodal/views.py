from flask import Blueprint
from flask import render_template

from .utils import Config

view = Blueprint("views", __name__)


@view.route("/")
def hello_world():
    return render_template("index.html", config=Config)
