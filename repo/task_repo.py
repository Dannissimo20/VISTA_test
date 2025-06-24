from typing import Type
from sqlalchemy import delete, insert, select, update
from database.database import DBWriter
from models.task_model import TaskModel
from schemas.task_schemas import TaskIn, TaskOut, TaskUpdate


class Task:
    def __init__(self, db: DBWriter):
        self.db: DBWriter = db

    @property
    def _table(self) -> Type[TaskModel]:
        return TaskModel


    def get_tasks(self) -> list[TaskOut]:
        query = select(self._table)
        with self.db.session() as session:
            res = session.execute(query).scalars().all()
            result = [TaskOut.model_validate(item) for item in res]
            return result
        
    
    def get_task_by_id(self, task_id: str) -> TaskOut:
        query = select(self._table).where(self._table.id == task_id)
        with self.db.session() as session:
            res = session.execute(query).scalar()
            return TaskOut.model_validate(res)
    

    def add_task(self, task: TaskIn):
        task_data = task.model_dump()
        query = insert(self._table).values(task_data).returning(self._table)
        with self.db.session() as session:
            session.execute(query)
            print("Task created")
            session.commit()
    

    def update_task(self, task_id: str, task: TaskUpdate):
        task_data = task.model_dump(exclude_unset=True)
        query = update(self._table).where(self._table.id == task_id).values(**task_data)
        with self.db.session() as session:
            session.execute(query)
            print(f"Task {task_id} updated")
            session.commit()

    
    def delete_task(self, task_id: str):
        query = delete(self._table).where(self._table.id == task_id)
        with self.db.session() as session:
            session.execute(query)
            print(f"Task {task_id} deleted")
            session.commit()


    def mark_checked(self, task_id: str):
        query = update(self._table).where(self._table.id == task_id).values(checked=True)
        with self.db.session() as session:
            session.execute(query)
            print(f"Task {task_id} checked")
            session.commit()

