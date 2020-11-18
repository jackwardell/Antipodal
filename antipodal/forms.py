from flask_wtf import FlaskForm
from flask_wtf import RecaptchaField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import InputRequired
from wtforms.validators import Length


class FeedbackForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(min=1, max=128)])
    email_address = StringField("Email Address")
    instagram_handle = StringField("Instagram Handle")
    twitter_handle = StringField("Twitter Handle")
    feedback = TextAreaField(
        "Feedback", validators=[InputRequired(), Length(min=1, max=2048)]
    )
    recaptcha = RecaptchaField("reCAPTCHA")
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
