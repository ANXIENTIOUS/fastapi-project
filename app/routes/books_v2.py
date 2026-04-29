from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional

from app.auth.dependencies import get_current_user

from app.db import get_session
from app.schemas import book as schema_book

router = APIRouter(
    prefix="/v2/books",
    tags=["Books DB"]
)


# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_book.BookRead)
def create_book(book: schema_book.BookCreate,
                session: Session = Depends(get_session)):

    new_book = schema_book.Book(
        title=book.title,
        author=book.author,
        year=book.year,
        description=book.description
    )

    session.add(new_book)
    session.commit()
    session.refresh(new_book)

    return new_book


# READ ALL
@router.get("/", response_model=List[schema_book.BookRead])
def read_books(
    title: Optional[str] = Query(default=None),
    author: Optional[str] = Query(default=None),
    session: Session = Depends(get_session)
):
    query = select(schema_book.Book)

    # Фильтр по названию
    if title:
        query = query.where(schema_book.Book.title.contains(title))

    # Фильтр по автору
    if author:
        query = query.where(schema_book.Book.author.contains(author))

    books = session.exec(query).all()

    if not books:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Book list is empty"
        )

    return books


# READ ONE
@router.get("/{book_id}", response_model=schema_book.BookRead)
def read_book(book_id: int,
              session: Session = Depends(get_session)):

    book = session.get(schema_book.Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book {book_id} not found"
        )

    return book


# UPDATE
@router.patch("/{book_id}", response_model=schema_book.BookRead)
def update_book(book_id: int,
                data_for_update: dict,
                session: Session = Depends(get_session)):

    book = session.get(schema_book.Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book {book_id} not found"
        )

    book_fields = set(schema_book.BookCreate.model_fields.keys())

    if not set(data_for_update.keys()) <= book_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Allowed fields: {', '.join(book_fields)}"
        )

    for key, value in data_for_update.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


# DELETE
@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int,
                session: Session = Depends(get_session)):

    book = session.get(schema_book.Book, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book {book_id} not found"
        )

    session.delete(book)
    session.commit()

    return {"message": f"Book {book_id} deleted"}
