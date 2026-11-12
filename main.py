
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task Manager API",
    description="A FastAPI application for managing tasks",
    version="1.0.0"
)

# Temporary in-memory storage
tasks = []

# Task schema
class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


@app.get("/")
def home():
    return {
        "message": "Welcome to Task Manager API",
        "status": "Running successfully"
    }


@app.get("/tasks")
def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.post("/tasks")
def create_task(task: Task):
    for existing_task in tasks:
        if existing_task["id"] == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task ID already exists"
            )

    tasks.append(task.model_dump())

    return {
        "message": "Task created successfully",
        "task": task
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            if updated_task.id != task_id:
                raise HTTPException(
                    status_code=400,
                    detail="Task ID cannot be changed"
                )

            tasks[index] = updated_task.model_dump()

            return {
                "message": "Task updated successfully",
                "task": updated_task
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return {
                "message": "Task deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )
