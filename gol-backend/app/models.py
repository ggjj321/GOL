import sqlalchemy as sa

from database import Base


class User(Base):
    __tablename__ = "user"

    id = sa.Column(sa.INTEGER, primary_key=True, nullable=False)
    create_at = sa.Column(sa.DATE, nullable=False)
    password = sa.Column(sa.VARCHAR(length=20), nullable=False)
    authority = sa.Column(sa.Enum(
        "Admin", "Developer", "Member", name="authority"), nullable=False)
    name = sa.Column(sa.VARCHAR(length=30), nullable=False)
    phone = sa.Column(sa.VARCHAR(length=20), nullable=False)
    email = sa.Column(sa.VARCHAR(length=100), nullable=False)
    member_balance = sa.Column(sa.INTEGER)


class Game(Base):
    __tablename__ = "game"

    game_id = sa.Column(sa.INTEGER,
                        primary_key=True, nullable=False)
    create_at = sa.Column(sa.DATE, nullable=False)
    game_name = sa.Column(sa.VARCHAR(length=20), nullable=False)
    game_sale_price = sa.Column(sa.INTEGER, nullable=False)
    game_developer = sa.Column(sa.VARCHAR(length=20), nullable=False)
    game_picture = sa.Column(sa.BLOB(), nullable=False)
    game_introduction = sa.Column(sa.VARCHAR(length=2000), nullable=False)
    game_discount = sa.Column(sa.DECIMAL())
    game_genre = sa.Column(sa.VARCHAR(length=50), nullable=False)
    game_version = sa.Column(sa.VARCHAR(length=20), nullable=False)
    game_developer_id = sa.Column(
        sa.INTEGER, sa.ForeignKey("user.id"), nullable=False)


class Cart(Base):
    __tablename__ = "cart"

    cart_id = sa.Column(sa.INTEGER,
                        primary_key=True, nullable=False)
    user_id = sa.Column(sa.INTEGER,
                        sa.ForeignKey("user.id"), nullable=False)
    game_id = sa.Column(sa.INTEGER, sa.ForeignKey(
        "game.game_id"), nullable=False)
    cost = sa.Column(sa.INTEGER, nullable=False)
    place_order = sa.Column(sa.Boolean, nullable=False)


class GameList(Base):
    __tablename__ = 'game_list'

    game_list_id = sa.Column(sa.INTEGER,
                             primary_key=True, nullable=False)
    create_at = sa.Column(sa.DATE, nullable=False)
    user_id = sa.Column(sa.INTEGER,
                        sa.ForeignKey("user.id"), nullable=False)
    game_list_type = sa.Column(
        sa.Enum("Wishlist", "Library", name="game_list_type"), nullable=False)
    comment = sa.Column(sa.VARCHAR(length=200))
    category = sa.Column(sa.VARCHAR(length=100))
    game_id = sa.Column(sa.INTEGER, sa.ForeignKey(
        "game.game_id"), nullable=False)


class Issue(Base):
    __tablename__ = 'issue'

    issue_id = sa.Column(sa.INTEGER,
                         primary_key=True, nullable=False)
    create_at = sa.Column(sa.DATE, nullable=False)
    issue_type = sa.Column(
        sa.Enum("Violation", "Refund", name="issue_type"), nullable=False)
    issue_deleted_at = sa.Column(sa.DATE)
    user_id = sa.Column(sa.INTEGER,
                        sa.ForeignKey("user.id"), nullable=False)
    violation_content = sa.Column(sa.VARCHAR(length=200))
    refund_acception = sa.Column(sa.Boolean)
    refund_gameId = sa.Column(sa.INTEGER,
                              sa.ForeignKey("game.game_id"), nullable=False)
