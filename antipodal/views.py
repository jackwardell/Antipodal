from flask import Blueprint
from flask import render_template
from .utils import page_hit

view = Blueprint("views", __name__)


@page_hit
@view.route("/")
def hello_world():
    return render_template("index.html")
