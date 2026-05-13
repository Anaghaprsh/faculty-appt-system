import pytest
import json
from app.app import app, faculty_db, appointments_db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        # Reset state before each test
        faculty_db["F001"]["available_slots"] = ["09:00", "11:00", "14:00"]
        faculty_db["F002"]["available_slots"] = ["10:00", "13:00", "15:00"]
        appointments_db.clear()
        yield client

# ─────────────────────────────────────────────
# Test: Home route
# ─────────────────────────────────────────────
def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["status"] == "running"

# ─────────────────────────────────────────────
# Test: Health check
# ─────────────────────────────────────────────
def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert json.loads(res.data)["status"] == "healthy"

# ─────────────────────────────────────────────
# Test: Get all faculty
# ─────────────────────────────────────────────
def test_get_all_faculty(client):
    res = client.get("/api/faculty")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "faculty" in data
    assert len(data["faculty"]) == 3

# ─────────────────────────────────────────────
# Test: Get specific faculty
# ─────────────────────────────────────────────
def test_get_faculty_valid(client):
    res = client.get("/api/faculty/F001")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["name"] == "Dr. Ramesh Kumar"

def test_get_faculty_invalid(client):
    res = client.get("/api/faculty/F999")
    assert res.status_code == 404

# ─────────────────────────────────────────────
# Test: Availability
# ─────────────────────────────────────────────
def test_get_availability(client):
    res = client.get("/api/faculty/F002/availability")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "available_slots" in data
    assert "10:00" in data["available_slots"]

# ─────────────────────────────────────────────
# Test: Book appointment - success
# ─────────────────────────────────────────────
def test_book_appointment_success(client):
    payload = {
        "student_name": "Anagha H Prashanth",
        "usn": "1DT23CS019",
        "faculty_id": "F001",
        "slot": "09:00"
    }
    res = client.post("/api/appointments",
                      data=json.dumps(payload),
                      content_type="application/json")
    assert res.status_code == 201
    data = json.loads(res.data)
    assert data["appointment"]["usn"] == "1DT23CS019"

# ─────────────────────────────────────────────
# Test: Book appointment - slot conflict
# ─────────────────────────────────────────────
def test_book_appointment_slot_conflict(client):
    payload = {
        "student_name": "Amisha AR",
        "usn": "1DT23CS015",
        "faculty_id": "F001",
        "slot": "09:00"
    }
    # Book once
    client.post("/api/appointments", data=json.dumps(payload), content_type="application/json")
    # Try booking same slot again
    res = client.post("/api/appointments", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 409

# ─────────────────────────────────────────────
# Test: Book appointment - missing fields
# ─────────────────────────────────────────────
def test_book_appointment_missing_field(client):
    payload = {"student_name": "Chinmayi Padmaraj", "faculty_id": "F001"}
    res = client.post("/api/appointments", data=json.dumps(payload), content_type="application/json")
    assert res.status_code == 400

# ─────────────────────────────────────────────
# Test: Get appointments
# ─────────────────────────────────────────────
def test_get_appointments(client):
    res = client.get("/api/appointments")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "appointments" in data
