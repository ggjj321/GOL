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
        create_at=datetime.datetime.now(), password=get_hashed_password(user.password), authority="Member", name=user.username, phone=user.phone, email=user.email, member_balance=0)
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
