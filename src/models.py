from pydantic import BaseModel
from typing import List, Optional


class Event(BaseModel):
    start: int
    stop: Optional[int] = None
    tags: List[str]


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
