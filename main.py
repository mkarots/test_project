from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

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

if __name__ == "__main__":
    logger.info("Starting Airway API server")
    uvicorn.run(app, host="0.0.0.0", port=8080)
