from pydantic import BaseModel, Field
from typing import Optional


class BookCreate(BaseModel):
    title: str = Field(
        description="Название книги",
        max_length=200
    )
    author: str = Field(
        description="Автор книги",
        max_length=100
    )
    year: int = Field(
        description="Год публикации",
        ge=0,
        le=2100
    )
    description: Optional[str] = Field(
        default=None,
        description="Краткое описание книги",
        max_length=1000
    )


class BookRead(BookCreate):
    book_id: int
