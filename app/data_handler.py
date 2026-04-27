import csv
import os
from typing import List, Optional
from app.schemas import book as schema_book

FILE_PATH = "books.csv"
FIELDNAMES = ["book_id", "title", "author", "year", "description"]


# --- Вспомогательная функция ---
def _ensure_file_exists():
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


# CREATE
def write_book_to_csv(book: schema_book.BookCreate) -> schema_book.BookRead:
    _ensure_file_exists()

    books = read_books_from_csv() or []

    # Генерация ID
    if books:
        new_id = max(b["book_id"] for b in books) + 1
    else:
        new_id = 1

    new_book = {
        "book_id": new_id,
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "description": book.description or ""
    }

    with open(FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(new_book)

    return schema_book.BookRead(**new_book)


# READ ALL
def read_books_from_csv() -> Optional[List[dict]]:
    _ensure_file_exists()

    with open(FILE_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        books = list(reader)

        if not books:
            return None

        # Преобразование типов
        for b in books:
            b["book_id"] = int(b["book_id"])
            b["year"] = int(b["year"])

        return books


# READ ONE
def read_book_from_csv(book_id: int) -> Optional[dict]:
    books = read_books_from_csv()

    if not books:
        return None

    for book in books:
        if book["book_id"] == book_id:
            return book

    return None


# UPDATE
def update_book_in_csv(book_id: int, data_for_update: dict) -> Optional[dict]:
    books = read_books_from_csv()

    if not books:
        return None

    updated = None

    for book in books:
        if book["book_id"] == book_id:
            for key, value in data_for_update.items():
                book[key] = value
            updated = book
            break

    if not updated:
        return None

    # Перезапись файла
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(books)

    return updated


# DELETE
def delete_book_from_csv(book_id: int) -> bool:
    books = read_books_from_csv()

    if not books:
        return False

    new_books = [b for b in books if b["book_id"] != book_id]

    if len(new_books) == len(books):
        return False  # ничего не удалилось

    # Перезапись файла без удалённой записи
    with open(FILE_PATH, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(new_books)

    return True
