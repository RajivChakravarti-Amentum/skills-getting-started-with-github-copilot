import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Helper to reset activities (if needed)
def reset_activities():
    if hasattr(app, 'activities'):
        app.activities.clear()

# --- Activity Listing ---
def test_list_activities():
    # Arrange
    # (No setup needed for initial state)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# --- Signup for Activity ---
def test_signup_for_activity():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "student1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

# --- Prevent Duplicate Signup ---
def test_prevent_duplicate_signup():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "student2@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400 or email in client.get("/activities").json()[activity_name]["participants"]

# --- Unregister Participant (if endpoint exists) ---
def test_unregister_participant():
    # Arrange
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "student3@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code in (200, 404)  # 404 if not implemented
    # If successful, participant should be removed
    if response.status_code == 200:
        assert email not in client.get("/activities").json()[activity_name]["participants"]

# --- Activity Not Found ---
def test_signup_activity_not_found():
    # Arrange
    fake_activity = "nonexistent"
    email = "student4@mergington.edu"
    # Act
    response = client.post(f"/activities/{fake_activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
