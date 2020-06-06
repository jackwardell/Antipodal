from flask import Blueprint
from flask import render_template
from flask import request

from .models import Feedback
from .utils import page_hit
from .utils import record_feedback

view = Blueprint("views", __name__)


@view.route("/")
@page_hit
def home():
    return render_template("calculate.html")


@view.route("/results")
@page_hit
def results():
    return render_template("results.html")


@view.route("/thanks_to")
@page_hit
def thanks_to():
    return render_template("thanks_to.html")


@view.route("/feedback", methods=["GET", "POST"])
@page_hit
def feedback():
    if request.method == "POST":
        record_feedback(
            name=request.form.get("input_name"),
            email_address=request.form.get("input_email_address"),
            instagram_handle=request.form.get("input_instagram_handle"),
            twitter_handle=request.form.get("input_twitter_handle"),
            feedback=request.form.get("input_feedback"),
        )
    return render_template("feedback.html")


# @view.route("/visitors")
# @page_hit
# def visitors():
#     return render_template("visitors.html")
