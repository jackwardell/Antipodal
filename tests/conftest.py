import pytest
from antipodal import create_app
from antipodal.models import db
from antipodal.utils import record_calculation,Location


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(testing=True)
    testing_client = flask_app.test_client()

    app_context = flask_app.app_context()
    app_context.push()

    db.create_all()

    yield testing_client

    app_context.pop()
