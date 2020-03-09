from flask import Blueprint
from flask import render_template
from .utils import page_hit

view = Blueprint("views", __name__)


@view.route("/")
@page_hit
def home():
    return render_template("calculate.html")


@view.route("/results")
@page_hit
def results():
    return render_template("results.html")
