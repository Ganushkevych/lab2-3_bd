"""
create_tables

Revision ID: 7ef5fc66e415
Revises: 
Create Date: 2023-12-28 17:12:51.466045

"""
from typing import Sequence, Union
from alembic import op
from models import Base

# revision identifiers, used by Alembic.
revision: str = '7ef5fc66e415'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    Base.metadata.create_all(op.get_bind())


def downgrade():
    Base.metadata.drop_all(op.get_bind())

