from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

import databases
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import uvicorn
# from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Book as SchemaBook
from schema import Author as SchemaAuthor
from schema import User as SchemaUser
from schema import Auth as SchemaAuth

from schema import Book
from schema import Author
from schema import User
from schema import Auth

from models import Book as ModelBook
from models import Author as ModelAuthor

import os
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

# DB related
# DATABASE_URL = "postgresql://username:password@localhost/db_name"
# DATABASE_URL = "postgresql://postgres:SellcaMocme2020@localhost/datacose"
DATABASE_URL = "postgresql://fito:fito@localhost/datacose"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Base = declarative_base()

# @app.on_event("startup")
# async def startup():
#     async with database.transaction():
#         Base.metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# @app.post("/items/")
# async def create_item(item: Item):
#     query = Item.__table__.insert().values(
#         name=item.name,
#         description=item.description
#     )
#     return await database.execute(query)


# @app.on_event("startup")
# async def startup() -> None:
#     database_ = app.state.database
#     if not database_.is_connected:
#         await database_.connect()

# @app.on_event("shutdown")
# async def shutdown() -> None:
#     database_ = app.state.database
#     if database_.is_connected:
#         await database_.disconnect()


@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    query = Item.__table__.select().where(Item.id == item_id)
    return await database.fetch_one(query)






# This will be used to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
