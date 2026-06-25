import re

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings


def _make_async_url(url: str) -> tuple:
    """Convert a psycopg2-style URL to asyncpg-compatible form.

    asyncpg doesn't accept sslmode/channel_binding query params — strip them
    and return ssl connect_args when the original URL required SSL.
    """
    needs_ssl = "sslmode=require" in url or "sslmode=verify" in url

    url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Remove params asyncpg doesn't understand
    url = re.sub(r"[?&]sslmode=[^&]*", "", url)
    url = re.sub(r"[?&]channel_binding=[^&]*", "", url)
    url = re.sub(r"\?&", "?", url)
    url = url.rstrip("?").rstrip("&")

    connect_args = {"ssl": "require"} if needs_ssl else {}
    return url, connect_args


_async_url, _connect_args = _make_async_url(settings.database_url)

engine = create_async_engine(_async_url, pool_pre_ping=True, connect_args=_connect_args)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
