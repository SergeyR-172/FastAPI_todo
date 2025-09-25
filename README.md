# FastAPI Todo App

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.43-blue)
![Docker](https://img.shields.io/badge/Docker-Supported-blue)

## 📝 Описание проекта

Проект предоставляет REST API для создания, чтения, обновления и удаления задач, а также возможность переключать статус выполнения задач. Приложение поддерживает работу с PostgreSQL и SQLite базами данных и может быть запущено как в контейнере Docker, так и локально.

## ✨ Особенности

- **Управление задачами** - создание, редактирование, удаление и просмотр задач
- **Статус задач** - возможность отмечать задачи как выполненные/невыполненные
- **Гибкая настройка базы данных** - поддержка PostgreSQL и SQLite с возможностью выбора через переменные окружения
- **API документация** - автоматическая генерация Swagger UI и ReDoc документации
- **Docker поддержка** - возможность запуска в контейнерах с PostgreSQL

## 🛠️ Технологии

- **FastAPI** 0.117.1 - современный веб-фреймворк для создания API
- **SQLAlchemy** 2.0.43 - ORM для работы с базой данных
- **Pydantic** 2.11.9 - валидация данных
- **PostgreSQL** - основная база данных (возможна работа с SQLite)
- **Docker** - для контейнеризации
- **Uvicorn** - ASGI сервер для запуска приложения

## 📁 Структура проекта

```
FastAPI_todo/
├── main.py                 # Основное приложение FastAPI
├── crud.py                 # Операции CRUD для задач
├── models.py               # Модели базы данных SQLAlchemy
├── schemas.py              # Pydantic схемы для валидации данных
├── database.py             # Настройки подключения к базе данных
├── init_db.py              # Инициализация базы данных
├── requirements.txt        # Зависимости проекта
├── Dockerfile              # Docker конфигурация
├── docker-compose.yml      # Конфигурация Docker Compose
├── .gitignore              # Файлы, исключенные из Git
├── favicon.ico             # Иконка приложения
└── README.md               # Документация проекта
```

## 🔧 Установка и запуск

### С использованием Docker (рекомендуется):

1. Клонируйте репозиторий:
```bash
git clone https://github.com/SergeyR-172/FastAPI_todo.git
cd FastAPI_todo
```

2. Запустите проект с помощью Docker Compose:
```bash
docker-compose up --build
```

Приложение будет доступно по адресу:
- API: `http://localhost:8000`
- API документация (Swagger): `http://localhost:8000/docs`
- ReDoc документация: `http://localhost:8000/redoc`

### Без Docker:

1. Установите Python 3.13 и PostgreSQL (или используйте SQLite)

2. Клонируйте репозиторий:
```bash
git clone https://github.com/SergeyR-172/FastAPI_todo.git
cd FastAPI_todo
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите инициализацию базы данных:
```bash
python init_db.py
```

5. Запустите приложение:
```bash
python main.py
```

Приложение будет доступно по адресу:
- API: `http://localhost:8000`
- API документация (Swagger): `http://localhost:8000/docs`
- ReDoc документация: `http://localhost:8000/redoc`

## 🌐 API эндпоинты

### Задачи:
- `POST /todos/` - создать новую задачу
- `GET /todos/{id}` - получить задачу по ID
- `GET /todos/` - получить список задач (с параметрами skip и limit)
- `PUT /todos/{id}` - полностью обновить задачу
- `PATCH /todos/{id}/toggle` - переключить статус выполнения задачи
- `DELETE /todos/{id}` - удалить задачу

### Документация:
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## 📋 Примеры использования API

### Создание задачи:
```json
POST /todos/
{
  "title": "Моя первая задача",
  "description": "Описание задачи",
  "completed": false
}
```

### Получение задачи по ID:
```
GET /todos/1/
```

### Получение списка задач:
```
GET /todos/?skip=0&limit=10
```

### Обновление задачи:
```json
PUT /todos/1/
{
  "title": "Обновленная задача",
  "description": "Новое описание",
  "completed": true
}
```

### Переключение статуса задачи:
```
PATCH /todos/1/toggle
```

### Удаление задачи:
```
DELETE /todos/1/
```

## ℹ️ Дополнительная информация

- Приложение автоматически использует SQLite, если переменные окружения для PostgreSQL не заданы
- Для работы с PostgreSQL задайте следующие переменные окружения:
 - `DB_USER` - имя пользователя базы данных
  - `DB_PASSWORD` - пароль пользователя
  - `DB_HOST` - хост базы данных
 - `DB_PORT` - порт базы данных
  - `DB_NAME` - имя базы данных
- Docker Compose автоматически создает базу данных при первом запуске