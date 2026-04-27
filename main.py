from fastapi import FastAPI
from app.routes import task

app = FastAPI(
    title="Система управления книгами",
    description="Простейшее API для управления списком книг (CSV), основанное на "
                "фреймворке FastAPI.",
    version="0.0.1",
    contact={
        "name": "Крестьянских Максим Григорьевич",
        "email": "krestianskikh.mg@phystech.edu",
    },
)

app.include_router(task.router)
