"""Adding updated_at attribute

Revision ID: e10f4973b9b7
Revises: dc2385c4d4d3
Create Date: 2025-06-13 13:09:52.943033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e10f4973b9b7'
down_revision: Union[str, None] = 'dc2385c4d4d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('update_at', postgresql.TIMESTAMP(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'update_at')
    # ### end Alembic commands ###
