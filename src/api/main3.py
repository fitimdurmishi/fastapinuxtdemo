from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from databases import Database
from fastapi.responses import JSONResponse

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import databases

import os
from dotenv import load_dotenv

load_dotenv('.env')

# DATABASE_URL = "postgresql://fito:fito@localhost/datacose"
DATABASE_URL = os.getenv("DATABASE_URL") # get it from .env
database = databases.Database(DATABASE_URL)

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



app = FastAPI()

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
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    if items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return items

# Create a new item
# @app.post("/items/")
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
