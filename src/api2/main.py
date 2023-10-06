from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
# from pydantic import BaseModel
# from typing import Optional
from datetime import datetime, timedelta

import datetime

from mypackage import crud, models, schemas
from mypackage.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



# ****** Auth related

# This will be used to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Replace this with your own user database or authentication logic
fake_users = {
    "testuser": {
        "username": "testuser",
        "password": "password"
    }
}

import os
from dotenv import load_dotenv

load_dotenv('.env')

SECRET_KEY = os.getenv("SECRET_KEY") # get it from .env file
ALGORITHM = os.getenv("ALGORITHM") # get it from .env file
ACCESS_TOKEN_EXPIRE_MINUTES_AS_STRING = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") # get it from .env file

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES_AS_STRING)
except ValueError as e:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return decode_token(token)


def create_jwt_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def authenticate_user(username: str, password: str):
    user = fake_users.get(username)
    if user is None or user['password'] != password:
        return None
    return user


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# ****** Auth endpoints

# @app.post("/token")
# def login_for_access_token(form_data: schemas.User):
#     user = authenticate_user(form_data.username, form_data.password)
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
#     access_token = create_jwt_token(data={"sub": user["username"]})
#     return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token")
def login(form_data: schemas.User):
    # Add your authentication logic here (e.g., username/password validation)
    # For simplicity, we'll just create a sample user
    #user = {"username": "testuser"}

    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


    access_token = create_access_token(data=user)
    return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/secure-data")
# def get_secure_data(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return {"message": "This is protected data!", "username": payload.get("sub")}
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@app.get("/secure-data")
def secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": "This is protected data", "user": current_user}




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