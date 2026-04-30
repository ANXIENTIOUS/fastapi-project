# Book Manager API

Простое веб-приложение для управления списком книг, реализованное на FastAPI.

---

## Об авторе

Студент МФТИ Крестьянских Максим Григорьевич, группа М02-505фя, почта krestyanskikh.mg@phystech.edu

---

## Функциональность

* CRUD операции с книгами (создание, чтение, обновление, удаление)
* Поиск книг по названию и автору
* JWT авторизация (регистрация и логин)
* Автоматические тесты

---

## Структура проекта

```
app/
├── main.py
├── db.py
├── routes/
│   ├── books_v2.py
│   └── auth.py
├── schemas/
│   ├── book.py
│   └── user.py
├── auth/
│   ├── utils.py
│   └── dependencies.py
```

---

## Установка и запуск

1. Клонировать репозиторий:

```
git clone https://github.com/ANXIENTIOUS/fastapi-project
cd fastapi-project
```

2. Создать виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate
```

3. Установить зависимости:

```
pip install fastapi uvicorn sqlmodel python-jose passlib[bcrypt] pytest
```

4. Запустить приложение:

```
fastapi dev main.py
```

---

## Документация API

После запуска доступна по адресу:

```
http://127.0.0.1:8000/docs
```

---

## Авторизация

### Регистрация

POST /auth/signup

Пример тела запроса:

```
{
  "email": "user@mail.com",
  "password": "123456",
  "name": "User"
}
```

---

### Логин

POST /auth/login

Используется форма (не JSON):

* username — email
* password — пароль

## Работа с книгами

### Создание книги

POST /v2/books

```
{
  "title": "1984",
  "author": "Джордж Оруэлл",
  "year": 1949,
  "description": "Антиутопия"
}
```

---

### Получение списка книг

GET /v2/books

---

### Поиск

```
/v2/books?title=1984
/v2/books?author=Оруэлл
```


### Обновление

PATCH /v2/books/{book_id}

---

### Удаление

DELETE /v2/books/{book_id}

---

## Тестирование

Запуск тестов:

```
pytest
```

---

## База данных

По умолчанию используется SQLite:

```
database.db
```

---

## Архитектура

* REST API
* Разделение на слои (routes, schemas, db)
* Dependency Injection (Depends)
* ORM через SQLModel

