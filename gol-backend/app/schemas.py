from datetime import datetime

from enum import Enum
from pydantic import BaseModel
from decimal import Decimal
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
    id: int
    create_at: datetime
    authority: Enum("authority", ["Admin", "Developer", "Member"])
    member_balance: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    username: Union[str, None] = None

# Game list
class OwnedGame(BaseModel):
    comment: str
    category: str
    game_id: int

class GameList(OwnedGame):
    game_list_id: int
    create_at: datetime = None
    user_id:  int
    game_list_type: Enum("game_list_type", ["Wishlist", "Library"])

    class Config:
        orm_mode = True

# Game
class GameDetail(BaseModel):
    game_sale_price: int
    game_developer: str
    game_picture: str = None
    game_introduction: str
    game_discount: Decimal 
    game_genre: str
    game_version: str
    game_developer_id: int

class Game(GameDetail):
    game_id: int
    create_at: datetime = None
    game_name: str

    class Config:
        orm_mode = True

# Cart
class Cart(BaseModel):
    cart_id: int
    user_id: int
    game_id: int
    cost: int
    place_order: bool

    class Config:
        orm_mode = True
        
# Issue
class Issue(BaseModel):
    issue_id: int
    create_at: datetime = None
    issue_type: Enum("issue_type", ["Violation", "Refund"])
    issue_deleted_at: datetime = None
    user_id: int
    violation_content: str
    refund_acception: bool
    refund_gameId: int

    class Config:
        orm_mode = True