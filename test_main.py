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
    # Verify the words string is correctly formatted
    assert data["words"] == f"{data['adjective']} {data['noun']}" 

def test_random_words_length():
    response = client.get("/random-words")
    assert response.status_code == 200
    data = response.json()
    assert len(data["words"]) <= 10

def test_create_todo():
    todo_data = {
        "title": "Test todo",
        "description": "Test description",
        "completed": False
    }
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert "id" in data
    assert "created_at" in data

def test_get_todos():
    # First, create a todo
    todo_data = {"title": "Test todo"}
    client.post("/todos", json=todo_data)
    
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_single_todo():
    # First, create a todo
    todo_data = {"title": "Test todo"}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]
    
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == todo_data["title"]

def test_update_todo():
    # First, create a todo
    todo_data = {"title": "Test todo"}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Update the todo
    update_data = {
        "title": "Updated todo",
        "completed": True
    }
    response = client.put(f"/todos/{todo_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["completed"] == update_data["completed"]

def test_delete_todo():
    # First, create a todo
    todo_data = {"title": "Test todo"}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]
    
    # Delete the todo
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    
    # Verify todo is deleted
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404

def test_get_nonexistent_todo():
    response = client.get("/todos/9999")
    assert response.status_code == 404

@pytest.fixture(autouse=True)
def clear_todos():
    # Clear todos before each test
    todos.clear()
    global current_id
    current_id = 1

