import datetime

from enum import Enum
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    password: str
    phone: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: str
    create_at: datetime.datetime
    authority:  Enum("authority", ["Admin", "Developer", "Member"])
    member_balance: int

    class Config:
        orm_mode = True
