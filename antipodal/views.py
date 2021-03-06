from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from .forms import FeedbackForm
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


@view.route("/thanks-to")
@page_hit
def thanks_to():
    return render_template("thanks_to.html")


@view.route("/feedback", methods=["GET", "POST"])
@page_hit
def feedback():
    form = FeedbackForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        record_feedback(**form.params)
        return redirect(url_for("views.feedback"))
    return render_template("feedback.html", form=form)


# @view.route("/visitors")
# @page_hit
# def visitors():
#     return render_template("visitors.html")
