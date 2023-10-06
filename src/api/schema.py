# build a schema using pydantic
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name:str
    description:str

    class Config:
        orm_mode = True

class Book(BaseModel):
    name: str
    page_numbers: int
    author_id: int

    class Config:
        orm_mode = True

class Author(BaseModel):
    name:str

    class Config:
        orm_mode = True

class User(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode = True

class Auth(BaseModel):
    user_id: int
    token: str

    class Config:
        orm_mode = True      
        