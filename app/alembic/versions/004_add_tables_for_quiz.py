"""Add tables for quiz

Revision ID: 004
Revises: 003
Create Date: 2025-03-24 16:03:17.876343

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '004'
down_revision: Union[str, None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quiz_users',
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('user_name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('user_id')
                    )
    op.create_table('quiz_results',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=True),
                    sa.Column('fumo_id', sa.Integer(), nullable=True),
                    sa.Column('fumo_count', sa.Integer(), nullable=True),
                    sa.Column('group_id', sa.BigInteger(), nullable=True),
                    sa.ForeignKeyConstraint(['fumo_id'], ['fumo.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['quiz_users.user_id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quiz_results')
    op.drop_table('quiz_users')
    # ### end Alembic commands ###
