import datetime

from enum import Enum
from pydantic import BaseModel
from typing import Union


class UserBase(BaseModel):
    username: str
    password: str


class UserLogIn(UserBase):
    pass


class UserCreate(UserBase):
    phone: str
    email: str


class User(UserCreate):
    id: str
    create_at: datetime.datetime
    authority:  Enum("authority", ["Admin", "Developer", "Member"])
    member_balance: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Union[str, None] = None
