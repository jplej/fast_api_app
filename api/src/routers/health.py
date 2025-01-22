from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.db import init_db, close_db
from src.redis import redis_client
from src.celery import celery_client
from src.routers import auth, users, questrade

router = APIRouter(
    prefix='/health',
    tags=['health']
)

class TaskData(BaseModel):
    process_name: str
    data: list
    

@router.get("/")
async def read_root():
    return {"status": "healthy"}


@router.get('/redis')
async def read_redis():
    redis_client.set('message', 'hello worls to redis...')
    message = redis_client.get('message')
    return {'message': message}
    
 
@router.post("/launch-celery-task")
def submit_task():
    data = {
        "process_name": "add",
        "data": [1, 2, 3, 4]
    }

    task = celery_client.send_task("handle_task", args=[data])
    return {"task_id": task.id, "status": "Task submitted"}

@router.get("/fetch-celery-task/{task_id}")
def get_task_result(task_id: str):
    task_result = celery_client.AsyncResult(task_id)

    if not task_result:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_result.state == "PENDING":
        return {"task_id": task_id, "status": "Task is still processing"}

    if task_result.state == "FAILURE":
        return {
            "task_id": task_id,
            "status": "Task failed",
            "error": str(task_result.info),
        }

    return {"task_id": task_id, "status": task_result.state, "result": task_result.result}