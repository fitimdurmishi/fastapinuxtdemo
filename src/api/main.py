from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# This will be used to get the token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    password: str

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

