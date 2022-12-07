from sqlalchemy.orm import Session

import models
import schemas

import datetime


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        create_at=datetime.datetime.now(), password=user.password, authority="Member", name=user.name, phone=user.phone, email=user.email, member_balance=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
