from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import init_db
from app.routes import books_v2
from app.routes import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(books_v2.router)
app.include_router(auth.router)
