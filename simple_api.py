from fastapi import FastAPI

app = FastAPI(
    title="Simple API",
    version="0.0.1"
)

@app.get("/")
async def root():
    return {"message": "Simple API v0.0.1"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) # Using a different port, e.g., 8001 