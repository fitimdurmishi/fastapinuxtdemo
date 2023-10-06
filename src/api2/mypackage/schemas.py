from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    class Config:
        orm_mode = True


class Author(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True


class Book(BaseModel):
    id: int
    name: str
    page_numbers: int
    author_id: int
    class Config:
        orm_mode = True

class User(BaseModel):
    id: int
    username: str
    password: str