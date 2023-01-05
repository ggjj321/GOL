from datetime import datetime
from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_

from decimal import Decimal

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
        "authority": logInUser.authority
    }


def get_user_info(db: Session, user: schemas.UserLogIn):
    result_user = db.query(models.User).filter(
        models.User.name == user.username).first()
    return schemas.User(
        username=result_user.name,
        email=result_user.email,
        password="x",
        phone=result_user.phone,
        id=result_user.id,
        create_at=str(result_user.create_at),
        authority=str(result_user.authority),
        member_balance=result_user.member_balance
    )


def update_user_authority(authority: str, db: Session, user: schemas.UserLogIn):
    need_change_user = db.query(models.User).filter(
        models.User.name == user.username)
    if not need_change_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{user.username} is not available')
    need_change_user.update(
        {
            "authority": authority
        }
    )
    db.commit()
    return user


def update_user_balance(add_money: int, db: Session, user: schemas.UserLogIn):
    need_change_user = db.query(models.User).filter(
        models.User.name == user.username)
    if not need_change_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{user.username} is not available')
    need_change_user.update(
        {
            "member_balance": need_change_user.first().member_balance + add_money
        }
    )
    db.commit()
    return user

# Game


def create_game(db: Session, user: schemas.UserLogIn, game: schemas.Game):
    developer = db.query(models.User).filter(
        models.User.name == user.username).first()
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
        game_developer_id=developer.id)

    db.add(created_game)
    db.commit()
    # db.refresh(created_game)
    return created_game


def get_game(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()


def get_game_by_genre(db: Session, genre: str, skip: int = 0, limit: int = 100):
    return db.query(models.Game).filter(models.Game.game_genre == genre).offset(skip).limit(limit).all()


def get_game_by_ID(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.game_id == game_id).first()


def update_game(db: Session, user: schemas.UserLogIn, game_id: int, UpdateGame: schemas.Game):
    info = models.Game(game_id=UpdateGame.game_id, create_at=UpdateGame.create_at, game_name=UpdateGame.game_name, game_sale_price=UpdateGame.game_sale_price, game_developer=UpdateGame.game_developer, game_picture=UpdateGame.game_picture,
                       game_introduction=UpdateGame.game_introduction, game_discount=UpdateGame.game_discount, game_genre=UpdateGame.game_genre, game_version=UpdateGame.game_version, game_developer_id=UpdateGame.game_developer_id)
    OldGame = db.query(models.Game).filter(models.Game.game_id == game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    OldGame.update(
        {
            "game_id": UpdateGame.game_id, "create_at": UpdateGame.create_at, "game_name": UpdateGame.game_name, "game_sale_price": UpdateGame.game_sale_price, "game_developer": UpdateGame.game_developer, "game_picture": UpdateGame.game_picture, "game_introduction": UpdateGame.game_introduction, "game_discount": UpdateGame.game_discount, "game_genre": UpdateGame.game_genre, "game_version": UpdateGame.game_version, "game_developer_id": UpdateGame.game_developer_id
        }
    )
    db.commit()
    return info


def update_game_name(db: Session, user: schemas.UserLogIn, game_id: int, name: str):
    OldGame = db.query(models.Game).filter(models.Game.game_id == game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    OldGame.update({"game_name": name})
    db.commit()
    return name


def update_game_price(db: Session, user: schemas.UserLogIn, game_id: int, price: int):
    OldGame = db.query(models.Game).filter(models.Game.game_id == game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    OldGame.update({"game_sale_price": price})
    db.commit()
    return price


def update_game_picture(db: Session, user: schemas.UserLogIn, game_id: int, pic: str):
    OldGame = db.query(models.Game).filter(models.Game.game_id == game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    OldGame.update({"game_picture": pic})
    db.commit()
    return pic


def update_game_info(db: Session, user: schemas.UserLogIn, game_id: int, info: str):
    OldGame = db.query(models.Game).filter(models.Game.game_id == game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    OldGame.update({"game_introduction": info})
    db.commit()
    return info


def update_game_discount(db: Session, user: schemas.UserLogIn, game_id: int, discount: Decimal):
    OldGame = db.query(models.Game).filter(models.Game.game_id == game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    OldGame.update({"game_discount": discount})
    db.commit()
    return discount


def update_game_version(db: Session, user: schemas.UserLogIn, game_id: int, version: str):
    OldGame = db.query(models.Game).filter(models.Game.game_id == game_id)
    if not OldGame.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    OldGame.update({"game_version": version})
    db.commit()
    return version


def delete_game(db: Session, user: schemas.UserLogIn, game_id: int):
    db_game_delete = db.query(models.Game).filter(
        models.Game.game_id == game_id).first()
    if not db_game_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Game with the id {game_id} is not available')
    db.delete(db_game_delete)
    db.commit()
    return True

# GameList


def create_gamelist_Lib(db: Session, user: schemas.UserLogIn, gamelist: schemas.GameList):
    add_game_user = db.query(models.User).filter(
        models.User.name == user.username).first()

    add_game = db.query(models.Game).filter(
        models.Game == gamelist.game_id).first()

    gamelist = models.GameList(
        game_list_id=gamelist.game_list_id,
        create_at=datetime.now(),
        user_id=add_game_user.id,
        game_list_type="Library",
        comment=gamelist.comment,
        category=add_game.game_genre,
        game_id=gamelist.game_id)

    db.add(gamelist)
    db.commit()
    return gamelist


def create_gamelist_Wish(db: Session, user: schemas.UserLogIn, gamelist: schemas.GameList):
    add_game_user = db.query(models.User).filter(
        models.User.name == user.username).first()

    add_game = db.query(models.Game).filter(
        models.Game.game_id == gamelist.game_id).first()

    gamelist = models.GameList(
        game_list_id=gamelist.game_list_id,
        create_at=datetime.now(),
        user_id=add_game_user.id,
        game_list_type="Wishlist",
        comment=gamelist.comment,
        category=add_game.game_genre,
        game_id=gamelist.game_id)

    db.add(gamelist)
    db.commit()
    return gamelist


def get_wishlist_games(db: Session, user: schemas.UserLogIn, skip: int = 0, limit: int = 100):
    want_get_list_user = db.query(models.User).filter(
        models.User.name == user.username).first()

    return db.query(models.User).\
        join(models.User.id).\
        join(models.GameList.game_id)

    # return db.query(models.User).\
    #     join(models.User.id).\
    #     join(models.GameList.game_id).\
    #     join(models.Game.game_id).\
    #     filter(models.User.id == want_get_list_user.id).\
    #     filter(models.GameList.game_list_type == "Wishlist")


def get_gamelist(db: Session, user: schemas.UserLogIn, skip: int = 0, limit: int = 100):
    return db.query(models.GameList).offset(skip).limit(limit).all()


def get_gamelist_by_type(db: Session, user: schemas.UserLogIn, type: str):
    userid = db.query(models.User.id).filter(
        models.User.name == user.username).first()
    return db.query(models.GameList).filter(models.GameList.game_list_type == type and models.GameList.user_id == userid).first()

# update needs to re-think


def update_gamelist_comment(db: Session, user: schemas.UserLogIn, gamelist_id: int, comment: str):
    userid = db.query(models.User.id).filter(
        models.User.name == user.username).first()
    Old = db.query(models.GameList).filter(
        models.GameList.game_list_id == gamelist_id)
    if not Old.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'GameList of the id {gamelist_id} is not available')
    Old.update({"comment": comment})
    db.commit()
    return comment


def update_gamelist_game(db: Session, user: schemas.UserLogIn, gamelist_id: int, game_id: int):
    userid = db.query(models.User.id).filter(
        models.User.name == user.username).first()
    Old = db.query(models.GameList).filter(
        models.GameList.game_list_id == gamelist_id)
    if not Old.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'GameList of the id {gamelist_id} is not available')
    Old.update({"game_id": game_id})
    db.commit()
    return game_id


def delete_gamelist(db: Session, user: schemas.UserLogIn, game_list_id: int):
    db_gamelist_delete = db.query(models.GameList).filter(
        models.GameList.game_list_id == game_list_id).first()
    if not db_gamelist_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'GameList with the id {game_list_id} is not available')
    db.delete(db_gamelist_delete)
    db.commit()
    return True

# CART


def create_cart(db: Session, user: schemas.UserLogIn, cart: schemas.Cart):
    want_by_game_user = db.query(models.User.id).filter(
        models.User.name == user.username).first()

    buyed_game = db.query(models.Game).filter(
        models.Game.game_id == cart.game_id).first()

    created_cart = models.Cart(
        cart_id=cart.cart_id,
        user_id=want_by_game_user.id,
        game_id=cart.game_id,
        cost=int(buyed_game.game_sale_price * (1 - buyed_game.game_discount)),
        place_order=False)

    db.add(created_cart)
    db.commit()
    return created_cart


def get_cart_or_lib(isLib: bool, db: Session, user: schemas.UserLogIn, skip: int = 0, limit: int = 100):
    userid = db.query(models.User.id).filter(
        models.User.name == user.username).first()

    all_game = db.query(models.Game).join(models.Cart, models.Game.game_id ==
                                          models.Cart.game_id).join(models.User, models.Cart.user_id ==
                                                                    userid.id).filter(models.Cart.place_order == isLib).offset(skip).limit(limit).all()

    return all_game


def update_cart_cost(db: Session, user: schemas.UserLogIn, game_id: int, cost: int):
    userid = db.query(models.User.id).filter(models.User.name == user.username)
    Old = db.query(models.Cart).filter(
        (models.Cart.user_id == userid) & (models.Cart.game_id == game_id))
    if not Old.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Cart of the id {user_id} is not available')
    Old.update({"cost": cost}, synchronize_session=False)
    db.commit()
    return game_id


def update_cart_place_order(db: Session, user: schemas.UserLogIn, game_id: int, place_order: bool):
    userid = db.query(models.User.id).filter(models.User.name == user.username)
    Old = db.query(models.Cart).filter(
        (models.Cart.user_id == userid) & (models.Cart.game_id == game_id))
    # if not Old.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f'Cart of the id {user_id} is not available')
    Old.update({"place_order": place_order}, synchronize_session=False)
    db.commit()
    return game_id


def delete_cart(db: Session, user: schemas.UserLogIn, gameID: int):
    buyer = db.query(models.User).filter(
        models.User.name == user.username)

    db_cart_delete = db.query(models.Cart).filter(
        models.Cart.game_id == gameID and models.User.id == buyer.id).first()
    if not db_cart_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Cart with the id  is not available')
    db.delete(db_cart_delete)
    db.commit()
    return True


def buy_single_game(db: Session, user: schemas.UserLogIn, gameID: int):
    buyer = db.query(models.User).filter(
        models.User.name == user.username)

    buyed_game = db.query(models.Game).filter(
        models.Game.game_id == gameID).first()

    if buyed_game.game_sale_price * (1 - buyed_game.game_discount) > buyer.first().member_balance:
        return "You don't have enough money"

    buyer.update({"member_balance": buyer.first().member_balance - (buyed_game.game_sale_price *
                 (1 - buyed_game.game_discount))}, synchronize_session=False)

    buyed_cart = db.query(models.Cart).filter(
        models.Cart.game_id == gameID and models.Cart.user_id == buyer.first().id)

    buyed_cart.update({"place_order": True}, synchronize_session=False)
    db.commit()
    return buyer


def buy_all_games(db: Session, user: schemas.UserLogIn, skip: int = 0, limit: int = 100):
    buyer = db.query(models.User).filter(
        models.User.name == user.username)

    buyed_carts = db.query(models.Game).join(
        models.Cart, models.Game.game_id == models.Cart.game_id).join(models.User, models.Cart.user_id == buyer.first().id).filter(models.Cart.place_order == False)

    total_money = 0
    update_cart_id = []

    for cart in buyed_carts:
        total_money += cart.game_sale_price * (1 - cart.game_discount)
        update_cart_id.append(cart.game_id)

    if total_money > buyer.first().member_balance:
        return "You don't have enough money"

    buyer.update({"member_balance": buyer.first().member_balance -
                 total_money}, synchronize_session=False)
    db.commit()

    for id in update_cart_id:
        buyed_cart = db.query(models.Cart).filter(
            models.Cart.game_id == id and models.Cart.user_id == buyer.first().id)
        buyed_cart.update({"place_order": True}, synchronize_session=False)
        db.commit()

    return buyer

# Issue


def create_issue_Violation(db: Session, user: schemas.UserLogIn, issue: schemas.Issue):
    created_issue = models.Issue(
        issue_id=issue.issue_id,
        create_at=datetime.now(),
        issue_type="Violation",
        issue_deleted_at=issue.issue_deleted_at,
        user_id=issue.user_id,
        violation_content=issue.violation_content,
        refund_acception=issue.refund_acception,
        refund_gameId=issue.refund_gameId)
    db.add(created_issue)
    db.commit()
    db.refresh(created_issue)
    return created_issue


def create_issue_Refund(db: Session, user: schemas.UserLogIn, issue: schemas.Issue):
    created_issue = models.Issue(
        issue_id=issue.issue_id,
        create_at=datetime.now(),
        issue_type="Refund",
        issue_deleted_at=issue.issue_deleted_at,
        user_id=issue.user_id,
        violation_content=issue.violation_content,
        refund_acception=issue.refund_acception,
        refund_gameId=issue.refund_gameId)
    db.add(created_issue)
    db.commit()
    db.refresh(created_issue)
    return created_issue


def get_issue(db: Session, user: schemas.UserLogIn, skip: int = 0, limit: int = 100):
    userid = db.query(models.User.id).filter(models.User.name == user.username)
    return db.query(models.Issue).filter(models.Issue.user_id == userid).offset(skip).limit(limit).all()


def update_issue_delete_date(db: Session, user: schemas.UserLogIn, issue_id: int, delete_date: datetime):
    userid = db.query(models.User.id).filter(models.User.name == user.username)
    Old = db.query(models.Issue).filter((models.Issue.issue_id == issue_id))
    if not Old.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Issue of the id {userid} is not available')
    Old.update({"issue_deleted_at": delete_date})
    db.commit()
    return delete_date


def update_issue_violation_content(db: Session, user: schemas.UserLogIn, issue_id: int, content: str):
    userid = db.query(models.User.id).filter(models.User.name == user.username)
    Old = db.query(models.Issue).filter((models.Issue.issue_id == issue_id))
    if not Old.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Issue of the id {userid} is not available')
    Old.update({"violation_content": content})
    db.commit()
    return content


def update_issue_refund_acception(db: Session, user: schemas.UserLogIn, issue_id: int, refund: bool):
    userid = db.query(models.User.id).filter(models.User.name == user.username)
    Old = db.query(models.Issue).filter((models.Issue.issue_id == issue_id))
    if not Old.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Issue of the id {userid} is not available')
    Old.update({"refund_acception": refund})
    db.commit()
    return refund


def delete_issue(db: Session, user: schemas.UserLogIn, issue_id: int):
    db_issue_delete = db.query(models.Issue).filter(
        models.Issue.issue_id == issue_id).first()
    if not db_issue_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Issue with the id {issue_id} is not available')
    db.delete(db_issue_delete)
    db.commit()
    return True
