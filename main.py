from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import os
from sqlalchemy.orm import Session

from database import SessionLocal
import crud as DB
from schemas import ToDoCreate, ToDoUpdate, ToDoGet

# Автоматическое закрытие соединения с базой
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="Todo API",
    description="API для управления задачами",
    version="1.0.0",
    openapi_tags=[
        {"name": "Задачи", "description": "Операции с задачами"},
        {"name": "Общее", "description": "Общие эндпоинты"}
    ]
)

@app.get(
    "/",
    response_class=HTMLResponse,
    summary="Главная страница",
    description="Возвращает приветственную страницу с информацией о приложении и ссылкой на документацию.",
    tags=["Общее"],
    operation_id="index"
)
def index():
    return HTMLResponse(content="<h1>FastAPI Todo App</h1><p>/docs для просмотра документации</p>")


@app.post(
    "/todos/",
    response_model=ToDoGet,
    summary="Создание новой задачи",
    description="Создает новую задачу с заголовком и описанием. Поле 'title' обязательно.",
    responses={
        201: {"description": "Задача успешно создана"},
        400: {"description": "Неверный запрос"},
    },
    tags=["Задачи"],
    status_code=status.HTTP_201_CREATED,
)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    return DB.create_todo(db, title=todo.title, description=todo.description)


@app.get(
    "/todos/{todo_id}",
    response_model=ToDoGet,
    summary="Получение одной задачи по ID",
    description="Возвращает задачу по заданному идентификатору. Если задача не найдена — возвращает ошибку 404.",
    responses={
        404: {"description": "Задача не найдена"},
        200: {"description": "Успешный ответ с задачей"},
    },
    tags=["Задачи"],
)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = DB.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.get(
    "/todos/",
    response_model=list[ToDoGet],
    summary="Получение списка задач",
    description="Возвращает список задач с возможностью пропуска первых N и ограничения по количеству.",
    tags=["Задачи"],
)
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = DB.get_todos(db, skip=skip, limit=limit)
    return todos


@app.put(
    "/todos/{todo_id}",
    response_model=ToDoGet,
    summary="Обновление задачи",
    description="Обновляет существующую задачу по ID. Если задача не найдена — возвращает ошибку 404.",
    responses={
        404: {"description": "Задача не найдена"},
        200: {"description": "Задача успешно обновлена"},
    },
    tags=["Задачи"],
)
def update_todo(todo_id: int, todo: ToDoUpdate, db: Session = Depends(get_db)):
    db_todo = DB.update_todo(
        db,
        todo_id=todo_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed
    )
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.delete(
    "/todos/{todo_id}",
    summary="Удаление задачи",
    description="Удаляет задачу по ID. Если задача не найдена — возвращает ошибку 404.",
    responses={
        404: {"description": "Задача не найдена"},
        200: {"description": "Задача успешно удалена"},
    },
    tags=["Задачи"],
)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    if not DB.delete_todo(db, todo_id=todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


@app.patch(
    "/todos/{todo_id}/toggle",
    response_model=ToDoGet,
    summary="Переключение статуса задачи (выполнено/не выполнено)",
    description="Меняет статус задачи с выполнено на не выполнено или наоборот. Если задача не найдена — возвращает ошибку 404.",
    responses={
        404: {"description": "Задача не найдена"},
        200: {"description": "Статус задачи успешно переключен"},
    },
    tags=["Задачи"],
)
def toggle_todo_status(todo_id: int, db: Session = Depends(get_db)):
    db_todo = DB.toggle_todo_status(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.get(
    "/favicon.ico",
    summary="Иконка для вкладки",
    description="Возвращает файл favicon.ico, чтобы убрать ошибку при обращении к иконке.",
    tags=["Общее"],
)
def favicon():
    file_path = "favicon.ico"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "favicon not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")
