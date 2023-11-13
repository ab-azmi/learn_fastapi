"""add content column

Revision ID: 5676128d7c84
Revises: 829a1ea1d8f7
Create Date: 2023-11-13 21:42:15.418035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5676128d7c84'
down_revision: Union[str, None] = '829a1ea1d8f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
