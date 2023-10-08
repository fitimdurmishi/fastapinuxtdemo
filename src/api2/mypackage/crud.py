from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models
from . import schemas


# Users table
def get_user_by_username_password(db: Session, username: str, password: str):
    return db.query(models.User).filter(models.User.username == username and models.User.password == password).first()


# Author table CRUDs
def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def get_author(db: Session, id: int):
    return db.query(models.Author).filter(models.Author.id == id).first()

def create_author(db: Session, author: schemas.Author):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, id: int, name: str):
    author = db.query(models.Author).filter(models.Author.id == id).first()
    if author is None:
        db.close()
        raise HTTPException(status_code=404, detail="Author not found")
    author.name = name
    db.commit()
    db.refresh(author)
    db.close()
    return author

def delete_author(db: Session, author_id: int):
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        db.close()
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    db.close()
    return author


# Books table CRUDs
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_books_by_author(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()

def get_book(db: Session, id: int):
    return db.query(models.Book).filter(models.Book.id == id).first()

def create_book(db: Session, book: schemas.Book):
    db_book = models.Book(name=book.name, page_numbers=book.page_numbers, author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, id: int, name: str, page_numbers: int, author_id: int):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if book is None:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")
    book.name = name
    book.page_numbers = page_numbers
    book.author_id = author_id
    db.commit()
    db.refresh(book)
    db.close()
    return book

def delete_book(db: Session, book_id: int):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    db.close()
    return book



# Items table
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()


def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, id: int, name: str, description: str):
    item = db.query(models.Item).filter(models.Item.id == id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = name
    item.description = description
    db.commit()
    db.refresh(item)
    db.close()
    return item


def delete_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    db.close()
    return item
