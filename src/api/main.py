from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from mypackage import crud, models, schemas
from mypackage.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# This will be used to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

import os
from dotenv import load_dotenv

load_dotenv('.env')
SECRET_KEY = os.getenv("SECRET_KEY") # get it from .env file
ALGORITHM = os.getenv("ALGORITHM") # get it from .env file


app = FastAPI()

# CORS related
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    user = crud.create_intial_user(db, "fito", "fito")
    return user


# ****** Auth endpoints and functions
def create_jwt_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_username_password(db, username=username, password=password)
    if user is None or user.password != password:
        return None
    return user

@app.post("/token")
def login_for_access_token(form_data: schemas.User, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_jwt_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure-data")
def get_secure_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": "This is protected data!", "username": payload.get("sub")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")




# ****** Authors API endpoints
@app.get("/authors/", response_model=list[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.Author, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, id=author.id)
    if db_author:
        raise HTTPException(status_code=400, detail="Author with this id already registered")
    return crud.create_author(db=db, author=author)

@app.put("/authors/{author_id}")
def update_author(author_id: int, author: schemas.Author, db: Session = Depends(get_db)):
    try:
        updated_author = crud.update_author(db, author_id, author.name)
        return {"message": "Author updated successfully", "author": updated_author}
    except HTTPException as e:
        return e
    
@app.delete("/authors/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    deleted_author = crud.delete_author(db, author_id)
    return {"message": "Author deleted successfully", "author": deleted_author}


# ****** Books API endpoints
@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books_by_author/{author_id}", response_model=list[schemas.Book])
def read_books_by_author(author_id: int, db: Session = Depends(get_db)):
    books = crud.get_books_by_author(db, author_id=author_id)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.Book, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, id=book.id)
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this id already registered")
    return crud.create_book(db=db, book=book)

@app.put("/books/{book_id}")
def update_book(book_id: int, book: schemas.Book, db: Session = Depends(get_db)):
    try:
        updated_book = crud.update_book(db, book_id, book.name, book.page_numbers, book.author_id)
        return {"message": "Book updated successfully", "book": updated_book}
    except HTTPException as e:
        return e
    
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = crud.delete_book(db, book_id)
    return {"message": "Book deleted successfully", "book": deleted_book}



# ****** Items API endpoints
@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, id=item.id)
    if db_item:
        raise HTTPException(status_code=400, detail="Item with this id already registered")
    return crud.create_item(db=db, item=item)

@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.Item, db: Session = Depends(get_db)):
    try:
        updated_item = crud.update_item(db, item_id, item.name, item.description)
        return {"message": "Item updated successfully", "item": updated_item}
    except HTTPException as e:
        return e
    
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted_item = crud.delete_item(db, item_id)
    return {"message": "Item deleted successfully", "item": deleted_item}