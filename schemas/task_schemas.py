from datetime import datetime
from pydantic import BaseModel


class TaskIn(BaseModel):
    title: str = "No name"
    text: str | None = None
    checked: bool = False

class TaskOut(BaseModel):
    id: str
    title: str
    text: str
    checked: bool
    createdat: datetime
    updatedat: datetime

    class Config:
        from_attributes=True