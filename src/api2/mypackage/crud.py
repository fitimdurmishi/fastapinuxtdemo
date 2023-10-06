from sqlalchemy.orm import Session
from fastapi import HTTPException

from . import models
from . import schemas

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
