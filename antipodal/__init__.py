from flask import Flask


def create_app():
    app = Flask(__name__)

    from .apis import api
    from .views import view
    app.register_blueprint(api)
    app.register_blueprint(view)

    return app
