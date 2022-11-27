"""create table

Revision ID: 32213d26087d
Revises: 
Create Date: 2022-11-19 15:24:07.423588

"""
from tokenize import String
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32213d26087d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column("Id", sa.VARCHAR(length = 20), primary_key = True, nullable = False),
        sa.Column("create_at", sa.DATE, nullable = False),
        sa.Column("password", sa.VARCHAR(length = 20), nullable = False),
        sa.Column("authority", sa.Enum("Admin", "Developer", "Member", name = "authority"), nullable = False),
        sa.Column("name", sa.VARCHAR(length = 30), nullable = False ),
        sa.Column("phone", sa.VARCHAR(length = 20), nullable = False),
        sa.Column("email", sa.VARCHAR(length = 100), nullable = False),
        sa.Column("member_balance", sa.INTEGER)
    )

    op.create_table(
        'game',
        sa.Column("game_id", sa.VARCHAR(length = 20), primary_key = True, nullable = False),
        sa.Column("create_at", sa.DATE, nullable = False),
        sa.Column("game_name", sa.VARCHAR(length = 20), nullable = False),
        sa.Column("game_sale_price", sa.INTEGER, nullable = False),
        sa.Column("game_developer", sa.VARCHAR(length = 20), nullable = False),
        sa.Column("game_picture", sa.BLOB(), nullable = False),
        sa.Column("game_introduction", sa.VARCHAR(length = 2000), nullable = False),
        sa.Column("game_discount", sa.DECIMAL()),
        sa.Column("game_genre", sa.VARCHAR(length = 50), nullable = False),
        sa.Column("game_version", sa.VARCHAR(length = 20), nullable = False),
        sa.Column("game_developer_id", sa.VARCHAR(length = 20), sa.ForeignKey("user.Id"), nullable = False)
    )

    op.create_table(
        'cart',
        sa.Column("cart_id", sa.VARCHAR(length = 20), primary_key = True, nullable = False),
        sa.Column("user_id", sa.VARCHAR(length = 20), sa.ForeignKey("user.Id"), nullable = False),
        sa.Column("game_id", sa.VARCHAR(length = 20), sa.ForeignKey("game.game_id"), nullable = False),
        sa.Column("cost", sa.INTEGER, nullable = False ),
        sa.Column("place_order", sa.Boolean, nullable = False )
    )

    op.create_table(
        'game_list',
        sa.Column("game_list_id", sa.VARCHAR(length = 20), primary_key = True, nullable = False),
        sa.Column("create_at", sa.DATE, nullable = False),
        sa.Column("user_id", sa.VARCHAR(length = 20), sa.ForeignKey("user.Id"), nullable = False ),
        sa.Column("game_list_type", sa.Enum("Wishlist", "Library", name = "game_list_type"), nullable = False),
        sa.Column("comment", sa.VARCHAR(length = 200)),
        sa.Column("category", sa.VARCHAR(length = 100)),
        sa.Column("game_id", sa.VARCHAR(length = 20), sa.ForeignKey("game.game_id"), nullable = False )
    )

    op.create_table(
        'issue',
        sa.Column("issue_id", sa.VARCHAR(length = 20), primary_key = True, nullable = False),
        sa.Column("create_at", sa.DATE, nullable = False),
        sa.Column("issue_type", sa.Enum("Violation", "Refund", name = "issue_type"), nullable = False),
        sa.Column("issue_deleted_at", sa.DATE),
        sa.Column("user_id", sa.VARCHAR(length = 20), sa.ForeignKey("user.Id"), nullable = False ),
        sa.Column("violation_content", sa.VARCHAR(length = 200)),
        sa.Column("refund_acception", sa.Boolean),
        sa.Column("refund_gameId", sa.VARCHAR(length = 20), sa.ForeignKey("game.game_id"), nullable = False )
    )

def downgrade() -> None:
    op.drop_table("user")
    op.drop_table("game")
    op.drop_table("cart")
    op.drop_table("game_list")
    op.drop_table("issue")