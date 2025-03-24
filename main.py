from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import logging
from datetime import datetime
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Airway API",
    description="Project management and deployment tool",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add word lists
ADJECTIVES = ['happy', 'bright', 'blue', 'clever', 'gentle', 'swift', 'bold', 'calm', 'kind', 'wise', 'sad', 'angry', 'excited', 'bored', 'hungry', 'thirsty', 'tired', 'sick', 'happy', 'sad', 'angry', 'excited', 'bored', 'hungry', 'thirsty', 'tired', 'sick']
NOUNS = ['cat', 'sun', 'tree', 'river', 'mountain', 'bird', 'book', 'cloud', 'star', 'flower', 'dog', 'car', 'house', 'computer', 'phone', 'food', 'water', 'sleep', 'work', 'play', 'movie', 'music', 'art', 'science', 'math', 'history', 'nature', 'travel', 'adventure', 'vacation', 'holiday']

# Todo model
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None

# In-memory storage for todos
todos = []
current_id = 1

@app.get("/")
async def root():
    logger.info("Received request to root endpoint")
    return {
        "message": "Welcome to Test Project",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    logger.info("Received health check request")
    return {
        "status": "healthy",
        "version": "0.1.0"
    }





@app.get("/datetime")
async def get_datetime():
    logger.info("Received request for current datetime")
    current_time = datetime.now()
    return {
        "datetime": current_time.isoformat(),
        "timezone": current_time.astimezone().tzinfo.tzname(current_time)
    }

@app.get("/random-words")
async def get_random_words():
    logger.info("Received request for random words")
    random_adj = random.choice(ADJECTIVES)
    random_noun = random.choice(NOUNS)
    return {
        "words": f"{random_adj} {random_noun}",
        "adjective": random_adj,
        "noun": random_noun
    }


@app.post("/todos", response_model=TodoItem)
async def create_todo(todo: TodoItem):
    logger.info("Creating new todo item")
    global current_id
    
    new_todo = todo.model_dump()
    new_todo["id"] = current_id
    new_todo["created_at"] = datetime.now()
    
    todos.append(new_todo)
    current_id += 1
    
    return new_todo

@app.get("/todos", response_model=List[TodoItem])
async def get_todos():
    logger.info("Fetching all todos")
    return todos

@app.get("/todos/{todo_id}", response_model=TodoItem)
async def get_todo(todo_id: int):
    logger.info(f"Fetching todo with id {todo_id}")
    todo = next((todo for todo in todos if todo["id"] == todo_id), None)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoItem)
async def update_todo(todo_id: int, todo_update: TodoItem):
    logger.info(f"Updating todo with id {todo_id}")
    todo_idx = next((idx for idx, todo in enumerate(todos) if todo["id"] == todo_id), None)
    if todo_idx is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_data = todo_update.model_dump(exclude_unset=True)
    update_data["id"] = todo_id
    update_data["created_at"] = todos[todo_idx]["created_at"]
    
    todos[todo_idx] = update_data
    return update_data


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    logger.info(f"Deleting todo with id {todo_id}")
    todo_idx = next((idx for idx, todo in enumerate(todos) if todo["id"] == todo_id), None)
    if todo_idx is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todos.pop(todo_idx)
    return {"message": "Todo deleted successfully"}


if __name__ == "__main__":
    logger.info("Starting Airway API server")
    uvicorn.run(app, host="0.0.0.0", port=8080)


