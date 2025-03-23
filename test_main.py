from fastapi.testclient import TestClient
from main import app
import pytest
from datetime import datetime

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Test Project",
        "status": "running"
    }

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "version": "0.1.0"
    }

def test_datetime():
    response = client.get("/datetime")
    assert response.status_code == 200
    data = response.json()
    
    # Check if the response contains required fields
    assert "datetime" in data
    assert "timezone" in data
    
    # Verify the datetime string can be parsed
    try:
        datetime.fromisoformat(data["datetime"])
    except ValueError:
        pytest.fail("Datetime string is not in valid ISO format")




def test_random_words():
    response = client.get("/random-words")
    assert response.status_code == 200
    data = response.json()
    
    # Check if the response contains required fields
    assert "words" in data
    assert "adjective" in data
    assert "noun" in data
    
    # Verify the adjective and noun are from our lists
    from main import ADJECTIVES, NOUNS
    assert data["adjective"] in ADJECTIVES
    assert data["noun"] in NOUNS
    
    # Verify the words string is correctly formatted
    assert data["words"] == f"{data['adjective']} {data['noun']}" 

def test_random_words_length():
    response = client.get("/random-words")
    assert response.status_code == 200
    data = response.json()
    assert len(data["words"]) <= 10

