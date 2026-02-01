"""add default to tasks.updated_at

Revision ID: 8bbb370dc15f
Revises: 224e6f6c1765
Create Date: 2026-02-01 15:22:06.754260

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bbb370dc15f'
down_revision: Union[str, None] = '224e6f6c1765'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "tasks",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.text("now()"),
        existing_nullable=False,
    )

    # fix any existing NULLs (just in case)
    op.execute("UPDATE tasks SET updated_at = created_at WHERE updated_at IS NULL;")



def downgrade() -> None:
    op.alter_column(
        "tasks",
        "updated_at",
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        existing_nullable=False,
    )
