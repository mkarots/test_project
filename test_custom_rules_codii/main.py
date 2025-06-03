from fastapi import FastAPI
import threading
import time
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# This function will be run in a separate thread
def long_running_task_in_thread(task_id: str, duration: int):
    logger.info(f"Threaded task '{task_id}' started for {duration} seconds.")
    time.sleep(duration)
    logger.info(f"Threaded task '{task_id}' finished.")

# Synchronous endpoint that uses a non-BackgroundTasks async mechanism (threading)
@app.post("/violate-rule/sync-endpoint-with-threading")
def sync_endpoint_with_threading_task(task_name: str = "default_task", delay: int = 3):
    """
    This endpoint is synchronous and uses Python's threading module
    to run a task, violating the rule:
    "* use async endpoints with fastapi and backgroundtasks for async tasks"
    """
    logger.info(f"Received request for synchronous endpoint with task: {task_name}")

    # Create and start a new thread for the "async" task
    # This is NOT using FastAPI's BackgroundTasks
    thread = threading.Thread(target=long_running_task_in_thread, args=(task_name, delay))
    thread.start()

    # The endpoint returns immediately, but the task runs in a separate thread
    return {
        "message": f"Synchronous endpoint initiated task '{task_name}' in a separate thread.",
        "rule_violation": "Endpoint is not async, and task uses 'threading' not 'BackgroundTasks'."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
