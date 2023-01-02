from datetime import datetime
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app.models import Game


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

#Game
def create_game(db: Session, game: schemas.Game, user: schemas.User):
    db_game = models.Game(
        game_sale_price=game.game_sale_price, 
        game_developer=game.game_developer, 
        game_picture=game.game_picture, 
        game_introduction=game.game_introduction, 
        game_discount=game.game_discount, 
        game_genre=game.game_genre, 
        game_version=game.game_version, 
        game_developer_id=game.game_developer_id, 
        game_id=game.game_id, 
        create_at=datetime.now(), 
        game_name=game.game_name
    )
    db.add(db_game)
    db.commit
    db.refresh(db_game)
    return db_game

def get_game(db:Session, skip: int = 0, limit: int = 100) -> Game:
    result = db.query(Game).offset(skip).limit(limit).all()
    db.commit()
    return result

def get_game_by_genre(db:Session, game: schemas.Game, game_genre:str) -> Game:
    result = db.query(Game).filter_by(game_genre = game_genre)
    db.commit()
    return result

def get_game_by_ID(db:Session, game: schemas.Game, game_id:int) -> Game:
    result = db.query(Game).filter_by(game_id = game_id).first()
    db.commit()
    return result

def update_game(db:Session, game: schemas.Game, game_id:int, _update_data = dict):
    result = db.query(Game).filter_by(game_id = game_id).update(_update_data)
    db.commit()
    return result
def update_game_name(db:Session, game: schemas.Game, game_id:int, _update_data = str):
    result =  db.query(Game).filter_by(game_id = game_id).update(_update_data)
    db.commit()
    return result

def update_game_price(db:Session, game: schemas.Game, game_id:int, _update_data = int):
    result =  db.query(Game).filter_by(game_id = game_id).update(_update_data)
    db.commit()
    return result

def update_game_picture(db:Session, game: schemas.Game, game_id:int, _update_data = str):
    result =  db.query(Game).filter_by(game_id = game_id).update(_update_data)
    db.commit()
    return result

def update_game_info(db:Session, game: schemas.Game, game_id:int, _update_data = str):
    result =  db.query(Game).filter_by(game_id = game_id).update(_update_data)
    db.commit()
    return result

def update_game_discount(db:Session, game: schemas.Game, game_id:int, _update_data = int):
    result =  db.query(Game).filter_by(game_id = game_id).update(_update_data)
    db.commit()
    return result

def update_game_version(db:Session, game: schemas.Game, game_id:int, _update_data = str):
    result =  db.query(Game).filter_by(game_id = game_id).update(_update_data)
    db.commit()
    return result

def delete_game(db:Session, game_id:int):
    result = db.query(Game).filter_by(game_id=game_id).delete()
    db.commit()
    return result