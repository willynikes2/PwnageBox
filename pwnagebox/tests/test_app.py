from fastapi.testclient import TestClient
from pwnagebox.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to PwnageBox"}

def test_perform_scan():
    response = client.post("/scan")
    assert response.status_code == 200
    assert "status" in response.json()

def test_perform_research():
    response = client.post("/research")
    assert response.status_code == 200
    assert "status" in response.json()

def test_perform_exploit():
    response = client.post("/exploit")
    assert response.status_code == 200
    assert "status" in response.json()

def test_perform_social_engineering():
    response = client.post("/social_engineering")
    assert response.status_code == 200
    assert "status" in response.json()
