from fastapi import Depends, FastAPI, HTTPException

from database.database import Base, DBWriter
from repo.task_repo import Task
from schemas.task_schemas import TaskIn, TaskOut, TaskUpdate


app = FastAPI()

db_writer = DBWriter()

Base.metadata.create_all(bind=db_writer.engine)


def get_task_repo() -> Task:
    return Task(db_writer)


@app.get("/get_all", response_model=list[TaskOut])
async def get_all(task_repo: Task = Depends(get_task_repo)):
    return task_repo.get_tasks()


@app.get("/get_by_id", response_model=TaskOut)
async def get_by_id(task_id: str, task_repo: Task = Depends(get_task_repo)):
    return task_repo.get_task_by_id(task_id)


@app.post("/add_task")
async def add_task(task: TaskIn, task_repo: Task = Depends(get_task_repo)):
    try:
        task_repo.add_task(task)
        return 200
    except Exception as e:
        print(e)
        raise HTTPException(500, "InternalServerError")
    

@app.put("/update_task")
async def update_task(task_id: str, task_data: TaskUpdate, task_repo: Task = Depends(get_task_repo)):
    try:
        task_repo.update_task(task_id, task_data)
        return 200
    except Exception as e:
        print(e)
        raise HTTPException(500, "InternalServerError")
    

@app.delete("/delete_task")
async def delete_task(task_id: str, task_repo: Task = Depends(get_task_repo)):
    try:
        task_repo.delete_task(task_id)
        return 200
    except Exception as e:
        print(e)
        raise HTTPException(500, "InternalServerError")