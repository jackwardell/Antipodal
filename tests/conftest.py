import os
import tempfile

import pytest

from antipodal import create_app
from antipodal.models import db


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    testing_client = flask_app.test_client()

    app_context = flask_app.app_context()
    app_context.push()
    db_file_directory, db_file = tempfile.mkstemp()
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_file
    flask_app.config["TESTING"] = True

    db.create_all()

    yield testing_client

    app_context.pop()

    os.close(db_file_directory)
    # os.unlink(flask_app.config["SQLALCHEMY_DATABASE_URI"])
