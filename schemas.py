from pydantic import BaseModel
from typing import Optional

class ToDoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class ToDoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class ToDoGet(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True