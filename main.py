from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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




if __name__ == "__main__":
    logger.info("Starting Airway API server")
    uvicorn.run(app, host="0.0.0.0", port=8080)


