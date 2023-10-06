# from fastapi import FastAPI
import psycopg2

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

import os
from dotenv import load_dotenv

app = FastAPI()

DB_HOST = "localhost"
DB_PORT = "5432"
DB_USER = "fito"
DB_PASSWORD = "fito"
DB_NAME = "datacose"

def connect_to_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

# import asyncpg

# async def connect_to_db_async():
#     conn = await asyncpg.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         user=DB_USER,
#         password=DB_PASSWORD,
#         database=DB_NAME
#     )
#     return conn



DATABASE_URL = "postgresql://fito:fito@localhost/datacose"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = create_engine(DATABASE_URL)



Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

@app.on_event("startup")
def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        database_.connect()

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