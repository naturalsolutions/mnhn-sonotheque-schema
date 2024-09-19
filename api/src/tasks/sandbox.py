from celery import shared_task
from fastapi import HTTPException
import time


@shared_task
def long_running_task(task_id: str):
    """
    A simple long-running task that can be launched from a FastAPI route.
    This task simulates work by sleeping for 10 seconds.
    """
    try:
        # Simulate some work
        time.sleep(10)
        return {"task_id": task_id, "status": "completed"}
    except Exception as e:
        # Log the error (you might want to use a proper logging system)
        print(f"Error in task {task_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task failed: {str(e)}")


# You can add more shared tasks here as needed
