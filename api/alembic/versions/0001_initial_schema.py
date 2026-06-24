"""Initial schema: origins, farms, auction_events, lots, certifications

Revision ID: 0001
Revises:
Create Date: 2026-06-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "origins",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("region", sa.String(200)),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        sa.Column("altitude_min_m", sa.Integer),
        sa.Column("altitude_max_m", sa.Integer),
        sa.Column("harvest_start_month", sa.Integer),
        sa.Column("harvest_end_month", sa.Integer),
        sa.Column("dominant_varietals", ARRAY(sa.Text)),
        sa.Column("flavor_tags", ARRAY(sa.Text)),
        sa.Column("notes", sa.Text),
    )
    op.create_index("ix_origins_country", "origins", ["country"])

    op.create_table(
        "farms",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("slug", sa.String(300), nullable=False, unique=True),
        sa.Column("canonical_name", sa.String(300), nullable=False),
        sa.Column("origin_id", sa.Integer, sa.ForeignKey("origins.id")),
        sa.Column("altitude_m", sa.Integer),
        sa.Column("varietals", ARRAY(sa.Text)),
        sa.Column("process_methods", ARRAY(sa.Text)),
        sa.Column("owner_name", sa.String(300)),
        sa.Column("cooperative_name", sa.String(300)),
        sa.Column("latitude", sa.Float),
        sa.Column("longitude", sa.Float),
        sa.Column("flavor_tags", ARRAY(sa.Text)),
        sa.Column("importer_ids", JSONB),
        sa.Column("source", sa.String(50)),
    )
    op.create_index("ix_farms_slug", "farms", ["slug"])
    op.create_index("ix_farms_canonical_name", "farms", ["canonical_name"])
    op.create_index("ix_farms_origin_id", "farms", ["origin_id"])
    # Full-text search index on name
    op.execute(
        "CREATE INDEX ix_farms_fts ON farms USING gin(to_tsvector('english', canonical_name))"
    )

    op.create_table(
        "auction_events",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("year", sa.Integer, nullable=False),
        sa.Column("event_name", sa.String(200)),
        sa.Column("event_date", sa.Date),
        sa.Column("origin_id", sa.Integer, sa.ForeignKey("origins.id")),
    )
    op.create_index("ix_auction_events_source", "auction_events", ["source"])
    op.create_index("ix_auction_events_country", "auction_events", ["country"])
    op.create_index("ix_auction_events_year", "auction_events", ["year"])

    op.create_table(
        "lots",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("auction_event_id", sa.Integer, sa.ForeignKey("auction_events.id")),
        sa.Column("farm_id", sa.Integer, sa.ForeignKey("farms.id")),
        sa.Column("lot_number", sa.Integer),
        sa.Column("score", sa.Numeric(4, 2)),
        sa.Column("process_method", sa.String(100)),
        sa.Column("varietal", ARRAY(sa.Text)),
        sa.Column("weight_kg", sa.Numeric(8, 2)),
        sa.Column("winning_price_usd_per_kg", sa.Numeric(8, 2)),
        sa.Column("buyer_name", sa.String(300)),
        sa.Column("flavor_tags", ARRAY(sa.Text)),
        sa.Column("tasting_notes", sa.Text),
        sa.Column("raw_source_data", JSONB),
    )
    op.create_index("ix_lots_auction_event_id", "lots", ["auction_event_id"])
    op.create_index("ix_lots_farm_id", "lots", ["farm_id"])
    op.create_index("ix_lots_score", "lots", ["score"])
    op.create_index("ix_lots_process_method", "lots", ["process_method"])
    op.create_index("ix_lots_buyer_name", "lots", ["buyer_name"])

    op.create_table(
        "certifications",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("farm_id", sa.Integer, sa.ForeignKey("farms.id"), nullable=False),
        sa.Column("body", sa.String(100), nullable=False),
        sa.Column("cert_number", sa.String(200)),
        sa.Column("valid_from", sa.Date),
        sa.Column("valid_until", sa.Date),
    )
    op.create_index("ix_certifications_farm_id", "certifications", ["farm_id"])


def downgrade() -> None:
    op.drop_table("certifications")
    op.drop_table("lots")
    op.drop_table("auction_events")
    op.drop_index("ix_farms_fts", "farms")
    op.drop_table("farms")
    op.drop_table("origins")
