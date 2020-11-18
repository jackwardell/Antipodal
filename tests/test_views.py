# import pytest


def test_home_view(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.data.decode()
    assert "Wardell's Antipode Namesake Coefficient" in data


def test_results_view(test_client):
    response = test_client.get("/results")
    assert response.status_code == 200
    data = response.data.decode()

    # check web page features
    assert "Wardell's Antipode Namesake Coefficient" in data
    assert "The Results" in data

    # check for table features
    assert '<table class="table table-bordered" id="results_table">' in data
    assert "</table>" in data
    # check data tables installed
    assert "dataTables.bootstrap4.min.js" in data
    assert "jquery.dataTables.js" in data
    assert "dataTables.bootstrap4.min.css" in data

    # add rows to table
    # record_calculation(
    #         location_a=Location(latitude=15.0, longitude=15.0, name="Hello"),
    #         location_b=Location(latitude=20.0, longitude=11.0, name="World"),
    #         is_namesake=True,
    #         antipode_coefficient=0.5
    #     )
    # record_calculation(
    #     location_a=Location(latitude=0.0, longitude=-5.0, name="Goodbye"),
    #     location_b=Location(latitude=-1.0, longitude=5.0, name="All"),
    #     is_namesake=False,
    #     antipode_coefficient=0.9
    # )


def test_thanks_to_view(test_client):
    response = test_client.get("/thanks-to")
    assert response.status_code == 200


def test_feedback_view_get(test_client):
    response = test_client.get("/feedback")
    assert response.status_code == 200


def test_feedback_view_post(test_client):
    name, feedback = "hello world", "this app is ok"
    response = test_client.get("/feedback")
    assert name not in response.data.decode()
    assert feedback not in response.data.decode()

    response = test_client.post("/feedback", data={"name": name, "feedback": feedback})
    assert response.status_code == 200
    assert name in response.data.decode()
    assert feedback in response.data.decode()
