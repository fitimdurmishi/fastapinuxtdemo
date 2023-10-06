from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

from databases import Database
from fastapi.responses import JSONResponse

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import databases

from schema import Book as SchemaBook
from schema import Author as SchemaAuthor
from schema import User as SchemaUser
from schema import Auth as SchemaAuth
from schema import Item as SchemaItem

from schema import Book
from schema import Author
from schema import User
from schema import Auth
from schema import Item

from models import Book as ModelBook
from models import Author as ModelAuthor
from models import Item as Item

import os
from dotenv import load_dotenv

load_dotenv('.env')

DATABASE_URL = os.getenv("DATABASE_URL") # get it from .env
database = databases.Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


app = FastAPI()

# This will be used to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/test_connection")
async def test_connection():
    try:
        # Execute a simple query to check the connection
        # query = "SELECT 1"
        query = "SELECT COUNT(*) FROM items"
        result = await database.fetch_val(query)
        if result > 0:
            return {"message": "Connection to PostgreSQL successful"}
        else:
            return {"message": "Failed to establish connection to PostgreSQL"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Connection error", "error": str(e)})



# Items related

# Get an items
@app.get("/items/")
# def read_items(token: str = Depends(oauth2_scheme)):
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    if items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return items


# Create a new item
# @app.post("/items", response_model=Item)
# def create_item(item: Item):
#     db = SessionLocal()
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     db.close()
#     return item

# @app.post("/items/")
# def create_item(item: Item):
#     db = SessionLocal()
#     db.query = Item.__table__.insert().values(
#         name=item.name,
#         description=item.description
#     )
#     # return database.execute(db.query)
#     database.execute(db.query)
#     return item

# Get an item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update an item
@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, description: str):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = name
    item.description = description
    db.commit()
    db.refresh(item)
    db.close()
    return item

# Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        db.close()
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    db.close()
    return {"message": "Item deleted"}





# This will be used to get the token from the request
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# class User(BaseModel):
#     username: str
#     password: str

# Replace this with your own user database or authentication logic
fake_users = {
    "testuser": {
        "username": "testuser",
        "password": "password"
    }
}

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

def create_jwt_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def authenticate_user(username: str, password: str):
    user = fake_users.get(username)
    if user is None or user['password'] != password:
        return None
    return user

@app.post("/token")
def login_for_access_token(form_data: User):
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_jwt_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure-data")
def get_secure_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": "This is protected data!", "username": payload.get("sub")}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
