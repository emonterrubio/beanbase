"""Add lot_rank to lots; unique constraints; importer_products table

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-25
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # lot_rank stores CoE-style rank strings: "1A", "1B", "NW", etc.
    op.add_column("lots", sa.Column("lot_rank", sa.String(20)))
    op.create_index("ix_lots_lot_rank", "lots", ["lot_rank"])

    # Unique constraint enables ON CONFLICT upserts in the CoE loader.
    # NULLs are not equal in PG unique constraints, so existing NULL-rank rows are unaffected.
    op.create_unique_constraint(
        "uq_lots_event_rank", "lots", ["auction_event_id", "lot_rank"]
    )

    # Enables SELECT-or-INSERT logic in coe_loader without race conditions.
    op.create_unique_constraint(
        "uq_auction_events_source_country_year",
        "auction_events",
        ["source", "country", "year"],
    )

    # Holds Onyx (and future) retail/importer product data that doesn't
    # resolve to a canonical farm (blends, multi-origin SKUs, etc.).
    op.create_table(
        "importer_products",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("variant_id", sa.String(100), nullable=False),
        sa.Column("title", sa.String(500)),
        sa.Column("product_type", sa.String(200)),
        sa.Column("sku", sa.String(200)),
        sa.Column("price_usd", sa.Numeric(8, 2)),
        sa.Column("available", sa.Boolean),
        sa.Column("origin", sa.String(200)),
        sa.Column("process", sa.String(100)),
        sa.Column("profile", sa.Text),
        sa.Column("scraped_month", sa.String(7), nullable=False),
        sa.Column("raw_data", JSONB),
    )
    op.create_index("ix_importer_products_source", "importer_products", ["source"])
    op.create_index("ix_importer_products_origin", "importer_products", ["origin"])
    op.create_unique_constraint(
        "uq_importer_products_source_variant_month",
        "importer_products",
        ["source", "variant_id", "scraped_month"],
    )


def downgrade() -> None:
    op.drop_table("importer_products")
    op.drop_constraint("uq_auction_events_source_country_year", "auction_events")
    op.drop_constraint("uq_lots_event_rank", "lots")
    op.drop_index("ix_lots_lot_rank", "lots")
    op.drop_column("lots", "lot_rank")
