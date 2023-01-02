from datetime import datetime
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app import models
from app import schemas

from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password,
)


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        create_at=datetime.now(), password=get_hashed_password(user.password), authority="Member", name=user.username, phone=user.phone, email=user.email, member_balance=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login(db: Session, user: schemas.UserLogIn):
    logInUser = db.query(models.User).filter(
        models.User.name == user.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect name or password"
        )

    if not verify_password(password=user.password, hashed_pass=logInUser.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect name or password"
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }

def create_game(db:Session,user:schemas.UserLogIn,game:schemas.Game):
    created_game = models.Game(
        game_id=game.game_id,
        create_at=datetime.now(),
        game_name=game.game_name,
        game_sale_price=game.game_sale_price,
        game_developer=user.username,
        game_picture=game.game_picture,
        game_introduction=game.game_introduction,
        game_discount=game.game_discount,
        game_genre=game.game_genre,
        game_version=game.game_version,
        game_developer_id=game.game_developer_id)

    db.add(created_game)
    db.commit()
    db.refresh(created_game)
    return created_game

def get_game(db:Session, skip:int=0,limit:int=100):
    return db.query(models.Game).offset(skip).limit(limit).all()

def get_game_by_genre(db:Session,genre:str,skip:int=0,limit:int=100):
    return db.query(models.Game).filter(models.Game.game_genre == genre).offset(skip).limit(limit).all()

def get_game_by_ID(db:Session, game_id:int):
    return db.query(models.Game).filter(models.Game.game_id == game_id).first()

def update_game(db:Session, user:schemas.UserLogIn, game_id:int, UpdateGame:schemas.Game):
    info = models.Game(
        game_id=UpdateGame.game_id,
        create_at=UpdateGame.create_at,
        game_name=UpdateGame.game_name,
        game_sale_price=UpdateGame.game_sale_price,
        game_developer=UpdateGame.game_developer,
        game_picture=UpdateGame.game_picture,
        game_introduction=UpdateGame.game_introduction,
        game_discount=UpdateGame.game_discount,
        game_genre=UpdateGame.game_genre,
        game_version=UpdateGame.game_version,
        game_developer_id=UpdateGame.game_developer_id)
    OldGame = db.query(models.Game).filter(models.Game.game_id==game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Game with the id {game_id} is not available')
    OldGame.update(
        {
            "game_id": UpdateGame.game_id,
            "create_at":UpdateGame.create_at,
            "game_name":UpdateGame.game_name,
            "game_sale_price":UpdateGame.game_sale_price,
            "game_developer":UpdateGame.game_developer,
            "game_picture":UpdateGame.game_picture,
            "game_introduction":UpdateGame.game_introduction,
            "game_discount":UpdateGame.game_discount,
            "game_genre":UpdateGame.game_genre,
            "game_version":UpdateGame.game_version,
            "game_developer_id":UpdateGame.game_developer_id
        }
    )
    db.commit()
    return info

