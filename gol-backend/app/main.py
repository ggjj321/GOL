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
from app.database import SessionLocal,engine

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



@app.post("/sign_up")
async def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/login")
async def user_login(user:  OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.login(db=db, user=user)


@app.get('/me', response_model=schemas.UserLogIn)
async def get_me(user: schemas.UserLogIn = Depends(get_current_user)):
    return user

##### NEED PART
###Game
#add game data
@app.post("/Game/add_game")
async def add_game(game:schemas.Game,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.create_game(db=db,user=user,game=game)

#get game data
@app.get("/Game/get_game_data")
async def get_games(skip:int = 0,limit:int=100, db:Session=Depends(get_db)):
    return crud.get_game(db=db,skip=skip,limit=limit)
#get game data by genre
@app.get("/Game/get_game_data_by_genre")
async def get_games(genre:str,skip:int = 0,limit:int=100, db:Session=Depends(get_db)):
    return crud.get_game_by_genre(db=db,skip=skip,limit=limit,genre=genre)
#get game data by id
@app.get("/Game/get_game_data_by_id")
async def get_game_by_ID(game_id:int,db:Session=Depends(get_db)):
    return crud.get_game_by_ID(db=db,game_id=game_id)
#add game all content
@app.patch("/Game/update_game",response_model=schemas.Game)
async def update_game(game_id:str,UpdateGame:schemas.Game,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_game(db,user,game_id,UpdateGame)
'''
#update game name
@app.patch("/Game/update_game_name",response_model=schemas.Game)
async def update_game_name(game_id:str,name:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_game_name(db,user,game_id,name)
#update game price
@app.patch("/Game/update_game_price",response_model=schemas.Game)
async def update_game_price(game_id:str,price:int,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_game_price(db,user,game_id,price)
#update game pic
@app.patch("/Game/update_game_pic",response_model=schemas.Game)
async def update_game_picture(game_id:str,pic:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_game_picture(db,user,game_id,pic)
#update game info
@app.patch("/Game/update_game_info",response_model=schemas.Game)
async def update_game_info(game_id:str,info:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_game_info(db,user,game_id,str)
#update game discount
@app.patch("/Game/update_game_discount",response_model=schemas.Game)
async def update_game_discount(game_id:str,discount:Decimal,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_game_discount(db,user,game_id,discount)
#update game version
@app.patch("/Game/update_game_version",response_model=schemas.Game)
async def update_game_version(game_id:str,version:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_game_version(db,user,game_id,version)
#delete game
@app.delete("/Game/delete_game",response_model=schemas.Game)
async def delete_game(game_id:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.delete_game(db,user,game_id)


###Game List
#add gamelist
@app.get("/GameList/add_gameslist")
async def add_gamelist(gamelist:schemas.GameList,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.create_gamelist(db,user,gamelist)
#get gamelist
@app.get("/GameList/get_gamelist", response_model=schemas.GameList)
async def get_gamelist(skip:int = 0,limit:int=100,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.get_gamelist(db,user,skip,limit)
#get gamelist by type
@app.get("/GameList/get_gamelist_by_type", response_model=schemas.GameList)
async def get_gamelist_by_type(type:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.get_gamelist_by_type(db,user,type)
#update gamelist comment
@app.patch("/GameList/update_gamelist_comment", response_model=schemas.GameList)
async def update_gamelist_comment(comment:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_gamelist_comment(db,user,comment)
#update gamelist game
@app.patch("/GameList/update_gamelist_game", response_model=schemas.GameList)
async def update_gamelist_game(game_id:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_gamelist_game(db,user,game_id)
#delete gamelist
@app.delete("/GameList/delete_gamelist",response_model=schemas.Game)
async def delete_gamelist(game_list_id:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.delete_gamelist(db,user,game_list_id)

###Cart
#add Cart
@app.get("/Cart/add_cart")
async def add_cart(cart:schemas.Cart,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.create_cart(db,user,cart)
#get Cart
@app.get("/Cart/get_cart", response_model=schemas.Cart)
async def get_cart(skip:int = 0,limit:int=100,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.get_cart(db,user,skip,limit)
#update cost
@app.patch("/Cart/update_cart_cost", response_model=schemas.Cart)
async def update_cart_cost(cost:int,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_cart_cost(db,user,cost)
#update place order
@app.patch("/Cart/update_cart_place_order", response_model=schemas.Cart)
async def update_cart_place_order(place_order:bool,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_cart_place_order(db,user,place_order)
#delete Cart
@app.delete("/Cart/delete_cart",response_model=schemas.Cart)
async def delete_cart(cart_id:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.delete_cart(db,user,cart_id)

###issue
#add Issue
@app.get("/Issue/add_issue")
async def add_issue(issue:schemas.Issue,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.create_issue(db,user,issue)
#get Issue
@app.get("/Issue/get_issue", response_model=schemas.Issue)
async def get_issue(skip:int = 0,limit:int=100,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.get_issue(db,user,skip,limit)
#update Issue delete date
@app.patch("/Issue/update_issue_delete_date", response_model=schemas.Issue)
async def update_issue_delete_date(delete_date:datetime,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_issue_delete_date(db,user,delete_date)
#update Issue violation content
@app.patch("/Issue/update_issue_violation_content", response_model=schemas.Issue)
async def update_issue_violation_content(content:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_issue_violation_content(db,user,content)
#update Issue violation content
@app.patch("/Issue/update_issue_refund_acception", response_model=schemas.Issue)
async def update_issue_refund_acception(refund:bool,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.update_issue_refund_acception(db,user,refund)
#delete Issue
@app.delete("/Issue/delete_issue",response_model=schemas.Issue)
async def delete_issue(issue_id:str,user: schemas.UserLogIn = Depends(get_current_user),db:Session=Depends(get_db)):
    return crud.delete_issue(db,user,issue_id)
'''