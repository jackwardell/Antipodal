import os

from flask import Flask
from flask_migrate import Migrate

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.testing = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_SITE_KEY")
    app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_SECRET_KEY")

    from .models import db
    from .apis import api
    from .views import view

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api)
    app.register_blueprint(view)

    return app
