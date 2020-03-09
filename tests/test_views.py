def test_home_view(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Wardell's Antipode Namesake Coefficient" in response.data


def test_results_view(test_client):
    response = test_client.get("/results")
    assert response.status_code == 200
    # check web page features
    assert b"Wardell's Antipode Namesake Coefficient" in response.data
    assert b"The Results" in response.data

    # check for table features
    assert b"<table id='results_table'>" and b"</table>" in response.data
    # check data tables installed
    assert b"dataTables.bootstrap4.min.js" in response.data
    assert b"jquery.dataTables.js" in response.data
    assert b"dataTables.bootstrap4.min.css" in response.data
