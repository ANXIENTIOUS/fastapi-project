from fastapi import APIRouter, status, HTTPException
from typing import List

from ..schemas import book as schema_book
from app.data_handler import (
    write_book_to_csv,
    read_books_from_csv,
    read_book_from_csv,
    update_book_in_csv,
    delete_book_from_csv
)

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_book.BookRead)
def create_book(book: schema_book.BookCreate):
    new_book = write_book_to_csv(book)
    return new_book


# READ ALL
@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[schema_book.BookRead])
def read_books():
    books = read_books_from_csv()

    if not books:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="The book list is empty."
        )

    return books


# READ ONE
@router.get("/{book_id}", response_model=schema_book.BookRead)
def read_book_by_id(book_id: int):
    book = read_book_from_csv(book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    return book


# UPDATE (PATCH)
@router.patch("/{book_id}", status_code=status.HTTP_200_OK,
              response_model=schema_book.BookRead)
def update_book_by_id(book_id: int, data_for_update: dict):

    book_fields = set(schema_book.BookCreate.model_fields.keys())

    if not set(data_for_update.keys()) <= book_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Allowed fields: {', '.join(book_fields)}"
        )

    book = update_book_in_csv(book_id, data_for_update)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    return book


# DELETE
@router.delete("/{book_id}", status_code=status.HTTP_200_OK)
def delete_book_by_id(book_id: int):

    deleted = delete_book_from_csv(book_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )

    return {"message": f"Book {book_id} deleted successfully"}
