from flask import Flask
from flask_migrate import Migrate

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    from .models import db
    from .apis import api
    from .views import view

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(api)
    app.register_blueprint(view)

    return app
