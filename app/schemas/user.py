from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    user_id: int
    email: EmailStr
    name: str
    
class User(SQLModel, table=True):
    user_id: int = Field(default=None, primary_key=True)
    email: str
    password_hash: str
    name: str
