from fastapi.testclient import TestClient
from main import app,history  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# TODO Add more tests

def test_get_history_empty():
    history.clear()
    response = client.get("/history")
    assert response.status_code ==200
    assert response.json() == []

def test_get_history_return_entries():
    history.clear()
    client.post("/calculate",params={"expr": "1+1"})
    response = client.get("/history")
    assert len(response.json()) == 1 

def test_get_history_limit():
    history.clear()
    for i in range(20):
        client.post("/calculate", params={"expr":f"{i}*2"})
    reponse = client.get("/history", params={"limit":10})
    assert len(reponse.json()) == 10

def test_delete_history():
    response = client.delete("/history")
    assert response.json() == {"ok": True, "cleared":True}

def test_delete_hist_clear_entries():
    client.post("/calculate", params={"expr":"5+5"})
    client.delete("/history")
    response = client.get("/history")
    assert response.json()==[]

def test_delete_code():
    response = client.delete("/history")
    assert response.status_code ==200