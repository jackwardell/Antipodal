from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    from .models import db
    from .apis import api
    from .views import view

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api)
    app.register_blueprint(view)

    return app
