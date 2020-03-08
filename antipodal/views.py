from flask import Blueprint
from flask import render_template
from .utils import page_hit

view = Blueprint("views", __name__)


@view.route("/")
@page_hit
def home():
    return render_template("index.html")
