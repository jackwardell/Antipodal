from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from wtforms.validators import Length


class FeedbackForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    email_address = StringField(
        "Email Address", validators=[InputRequired(), Length(min=3, max=128)]
    )
    instagram_handle = StringField("Instagram Handle", validators=[InputRequired()])
    twitter_handle = StringField("Twitter Handle", validators=[InputRequired()])
    feedback = TextAreaField("Feedback", validators=[InputRequired()])
    submit = SubmitField("Submit")

    @property
    def params(self):
        rv = {
            "name": self.name.data,
            "email_address": self.email_address.data,
            "instagram_handle": self.instagram_handle.data,
            "twitter_handle": self.twitter_handle.data,
            "feedback": self.feedback.data,
        }
        return rv
