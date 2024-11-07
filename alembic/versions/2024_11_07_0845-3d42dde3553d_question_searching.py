"""question_searching

Revision ID: 3d42dde3553d
Revises: 2583d6297e54
Create Date: 2024-11-07 08:45:37.119093

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d42dde3553d"
down_revision: Union[str, None] = "2583d6297e54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.create_index(
        "ix_question_content_trgm",
        "question",
        ["content"],
        postgresql_using="gin",
        postgresql_ops={"content": "gin_trgm_ops"},
    )


def downgrade():
    op.drop_index("ix_question_content_trgm", table_name="question")
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
