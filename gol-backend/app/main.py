from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import JWTError, jwt
from typing import Union, Any
from decimal import Decimal

from datetime import datetime
from app import crud
from app import models
from app import schemas
from app.database import SessionLocal, engine

from app.utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(
        models.User.name == token_data.username).first()
    if user is None:
        raise credentials_exception
    return schemas.UserLogIn(username=user.name, password="validate")


@app.get("/user_info")
async def user_info(user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_user_info(db=db, user=user)


@app.post("/sign_up")
async def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/login")
async def user_login(user:  OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.login(db=db, user=user)


@app.get('/me', response_model=schemas.UserLogIn)
async def get_me(user: schemas.UserLogIn = Depends(get_current_user)):
    return user


@app.post("/change_user_authority")
async def change_user_authority(authority: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_user_authority(authority=authority, db=db, user=user)

# NEED PART
# Game
# add game data


@app.post("/Game/add_game")
async def add_game(game: schemas.Game, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_game(db=db, user=user, game=game)

# get game data


@app.get("/Game/get_game_data")
async def get_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_game(db=db, skip=skip, limit=limit)
# get game data by genre


@app.get("/Game/get_game_data_by_genre")
async def get_games(genre: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_game_by_genre(db=db, skip=skip, limit=limit, genre=genre)
# get game data by id


@app.get("/Game/get_game_data_by_id")
async def get_game_by_ID(game_id: int, db: Session = Depends(get_db)):
    return crud.get_game_by_ID(db=db, game_id=game_id)
# add game all content


@app.patch("/Game/update_game")
async def update_game(game_id: int, UpdateGame: schemas.Game, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_game(db=db, user=user, game_id=game_id, UpdateGame=UpdateGame)

# update game name


@app.patch("/Game/update_game_name")
async def update_game_name(game_id: int, name: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_game_name(db=db, user=user, game_id=game_id, name=name)
# update game price


@app.patch("/Game/update_game_price")
async def update_game_price(game_id: int, price: int, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_game_price(db=db, user=user, game_id=game_id, price=price)
# update game pic


@app.patch("/Game/update_game_pic")
async def update_game_picture(game_id: int, pic: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_game_picture(db=db, user=user, game_id=game_id, pic=pic)
# update game info


@app.patch("/Game/update_game_info")
async def update_game_info(game_id: int, info: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_game_info(db=db, user=user, game_id=game_id, info=info)
# update game discount


@app.patch("/Game/update_game_discount")
async def update_game_discount(game_id: int, discount: Decimal, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_game_discount(db=db, user=user, game_id=game_id, discount=discount)
# update game version


@app.patch("/Game/update_game_version")
async def update_game_version(game_id: int, version: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_game_version(db=db, user=user, game_id=game_id, version=version)
# delete game


@app.delete("/Game/delete_game")
async def delete_game(game_id: int, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.delete_game(db, user, game_id)


# Game List
# add gamelist
@app.post("/GameList/add_gameslist_Lib")
async def add_gamelist(gamelist: schemas.GameList, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_gamelist_Lib(db=db, user=user, gamelist=gamelist)
# add gamelist Wishlist


@app.post("/GameList/add_gameslist_wish")
async def add_gamelist(gamelist: schemas.GameList, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_gamelist_Wish(db=db, user=user, gamelist=gamelist)
# get gamelist


@app.get("/GameList/get_gamelist")
async def get_gamelist(skip: int = 0, limit: int = 100, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_gamelist(db=db, user=user, skip=skip, limit=limit)
# get gamelist by type


@app.get("/GameList/get_gamelist_by_type")
async def get_gamelist_by_type(type: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_gamelist_by_type(db=db, user=user, type=type)

# update needs to re-think
# update gamelist comment


@app.patch("/GameList/update_gamelist_comment")
async def update_gamelist_comment(gamelist_id: int, comment: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_gamelist_comment(db=db, user=user, gamelist_id=gamelist_id, comment=comment)
# update gamelist game


@app.patch("/GameList/update_gamelist_game")
async def update_gamelist_game(gamelist_id: int, game_id: int, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_gamelist_game(db=db, user=user, gamelist_id=gamelist_id, game_id=game_id)

# delete gamelist


@app.delete("/GameList/delete_gamelist")
async def delete_gamelist(game_list_id: int, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.delete_gamelist(db=db, user=user, game_list_id=game_list_id)

# Cart
# add Cart


@app.post("/Cart/add_cart")
async def add_cart(cart: schemas.Cart, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_cart(db=db, user=user, cart=cart)
# get Cart


@app.get("/Cart/get_cart")
async def get_cart(skip: int = 0, limit: int = 100, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_cart(db=db, user=user, skip=skip, limit=limit)
# update cost


@app.patch("/Cart/update_cart_cost")
async def update_cart_cost(game_id: int, cost: int, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_cart_cost(db=db, user=user, game_id=game_id, cost=cost)
# update place order


@app.patch("/Cart/update_cart_place_order")
async def update_cart_place_order(game_id: int, place_order: bool, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_cart_place_order(db=db, user=user, game_id=game_id, place_order=place_order)
# delete Cart


@app.delete("/Cart/delete_cart")
async def delete_cart(cart_id: int, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.delete_cart(db=db, user=user, cart_id=cart_id)

# issue
# add Issue


@app.post("/Issue/add_issue_Vio")
async def add_issue(issue: schemas.Issue, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_issue_Violation(db=db, user=user, issue=issue)


@app.post("/Issue/add_issue_Refund")
async def add_issue(issue: schemas.Issue, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_issue_Refund(db=db, user=user, issue=issue)
# get Issue


@app.get("/Issue/get_issue")
async def get_issue(skip: int = 0, limit: int = 100, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_issue(db=db, user=user, skip=skip, limit=limit)
# update Issue delete date


@app.patch("/Issue/update_issue_delete_date")
async def update_issue_delete_date(issue_id: int, delete_date: datetime, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_issue_delete_date(db=db, user=user, delete_date=delete_date, issue_id=issue_id)
# update Issue violation content


@app.patch("/Issue/update_issue_violation_content")
async def update_issue_violation_content(issue_id: int, content: str, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_issue_violation_content(db=db, user=user, content=content, issue_id=issue_id)
# update Issue violation content


@app.patch("/Issue/update_issue_refund_acception")
async def update_issue_refund_acception(issue_id: int, refund: bool, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.update_issue_refund_acception(db=db, user=user, refund=refund, issue_id=issue_id)
# delete Issue


@app.delete("/Issue/delete_issue")
async def delete_issue(issue_id: int, user: schemas.UserLogIn = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.delete_issue(db=db, user=user, issue_id=issue_id)
