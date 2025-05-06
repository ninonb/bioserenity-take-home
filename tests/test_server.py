from fastapi.testclient import TestClient
from pymongo import MongoClient
import pytest
from server import app

client = TestClient(app)
mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['event_db']
events_collection = db['events']


@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: Clear the database before each test
    events_collection.delete_many({})
    yield
    # Teardown: Clear the database after each test
    events_collection.delete_many({})


def test_add_event():
    response = client.post("/add_event", json={"start": 1622547800, "stop": 1622551400, "tags": ["tag1", "tag2"]})
    assert response.status_code == 200
    assert response.json() == {"message": "Event added successfully"}


def test_list_events():
    client.post("/add_event", json={"start": 1622547800, "stop": 1622551400, "tags": ["tag1", "tag2"]})
    response = client.get("/list_events")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 1
    assert events[0]["start"] == 1622547800
    assert events[0]["stop"] == 1622551400
    assert events[0]["tags"] == ["tag1", "tag2"]


def test_remove_events():
    client.post("/add_event", json={"start": 1622547800, "stop": 1622551400, "tags": ["tag1", "tag2"]})
    response = client.delete("/remove_events")
    assert response.status_code == 200
    assert response.json() == {"message": "All events removed successfully"}
    response = client.get("/list_events")
    assert response.status_code == 200
    assert response.json() == []