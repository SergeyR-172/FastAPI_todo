from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import os



app = FastAPI()

@app.get("/")
def index():
    return HTMLResponse("Hello world")

# Устанавливаем иконку, чтобы убрать ошибку при орбращении к ней
@app.get("/favicon.ico")
def favicon():
    file_path = "favicon.ico"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "favicon not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000, host="0.0.0.0")