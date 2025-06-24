import binascii
import os
import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, String, func
from database.database import Base


class TaskModel(Base):
    __tablename__ = "task"

    id = Column(
        String(16),
        primary_key=True,
        default=lambda: binascii.hexlify(os.urandom(8)).decode()
    )
    
    title = Column(String)
    text = Column(String)
    checked = Column(Boolean, nullable=False, default=False)
    createdat = Column(DateTime, server_default=func.now())
    updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())
