def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"LoanHub" in response.data

def test_calculator_page(client):
    response = client.get("/calculator")
    assert response.status_code == 200
    assert b"Loan Calculator" in response.data
