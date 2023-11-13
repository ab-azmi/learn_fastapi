"""create post table

Revision ID: 829a1ea1d8f7
Revises: 
Create Date: 2023-11-13 21:31:08.157315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '829a1ea1d8f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(length=100), nullable=False))
    pass

def downgrade() -> None:
    op.drop_table('posts')
    pass
