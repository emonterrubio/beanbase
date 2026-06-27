"""Add importer lot-title fields to farms

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-26
"""

from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("farms", sa.Column("municipality", sa.String(200)))
    op.add_column("farms", sa.Column("department", sa.String(200)))
    op.add_column("farms", sa.Column("lot_varietal", sa.String(200)))
    op.add_column("farms", sa.Column("lot_process", sa.String(200)))
    op.add_column("farms", sa.Column("packaging_type", sa.String(100)))
    op.add_column("farms", sa.Column("source_lot_title", sa.String(500)))


def downgrade() -> None:
    op.drop_column("farms", "source_lot_title")
    op.drop_column("farms", "packaging_type")
    op.drop_column("farms", "lot_process")
    op.drop_column("farms", "lot_varietal")
    op.drop_column("farms", "department")
    op.drop_column("farms", "municipality")
