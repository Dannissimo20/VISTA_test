from sqlalchemy import UUID, Boolean, Column, DateTime, String
from database.database import Base


class TaskModel(Base):
    __tablename__ = "task"
    id = Column(UUID, primary_key = True)
    title = Column(String)
    text = Column(String)
    checked = Column(Boolean)
    createdat = Column(DateTime)
    updatedat = Column(DateTime)
