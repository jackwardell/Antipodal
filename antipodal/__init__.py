from flask import Flask
from flask_migrate import Migrate
import os

migrate = Migrate()


def create_app(testing: bool = False):
    app = Flask(__name__)
    if not testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory"

    from .models import db
    from .apis import api
    from .views import view

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api)
    app.register_blueprint(view)

    return app
