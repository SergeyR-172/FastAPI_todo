from sqlalchemy.orm import Session
from models import ToDo
from typing import List, Optional


def create_todo(db: Session, title: str, description: Optional[str] = None) -> ToDo:
    todo = ToDo(title=title, description=description, completed=False)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_todo(db: Session, todo_id: int) -> Optional[ToDo]:
    return db.query(ToDo).filter(ToDo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100) -> List[ToDo]:
    return db.query(ToDo).offset(skip).limit(limit).all()


def update_todo(
    db: Session, 
    todo_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    completed: Optional[bool] = None
) -> Optional[ToDo]:
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if todo:
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if completed is not None:
            todo.completed = completed
        db.commit()
        db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int) -> bool:
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
        return True
    return False


def toggle_todo_status(db: Session, todo_id: int) -> Optional[ToDo]:
    todo = db.query(ToDo).filter(ToDo.id == todo_id).first()
    if todo:
        todo.completed = not todo.completed
        db.commit()
        db.refresh(todo)
    return todo