from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import JWTError, jwt
from typing import Union, Any

import datetime
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


@app.post("/sign_up")
async def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.post("/login")
async def user_login(user:  OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return crud.login(db=db, user=user)


@app.post('/me', response_model=schemas.UserLogIn)
async def get_me(user: schemas.UserLogIn = Depends(get_current_user)):
    return user
