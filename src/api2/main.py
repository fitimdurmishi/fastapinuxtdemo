from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from mypackage import crud, models, schemas
from mypackage.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




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