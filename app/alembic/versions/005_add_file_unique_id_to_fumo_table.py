"""add file_unique_id to fumo table

Revision ID: 005
Revises: 004
Create Date: 2025-04-18 10:17:05.599502

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("fumo", schema=None) as batch_op:
        batch_op.add_column(sa.Column("file_unique_id", sa.String(), nullable=True))
        batch_op.create_unique_constraint("uq_fumo_file_unique_id", ["file_unique_id"])


def downgrade():
    with op.batch_alter_table("fumo", schema=None) as batch_op:
        batch_op.drop_constraint("uq_fumo_file_unique_id", type_="unique")
        batch_op.drop_column("file_unique_id")
