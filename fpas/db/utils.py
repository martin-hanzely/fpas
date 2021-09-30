from urllib.parse import urlparse

from sqlalchemy.sql import functions
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(functions.FunctionElement):
    type = DateTime  # type: ignore[assignment]


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


def async_postgres_dsn(dsn: str):
    """
    Replace DSN scheme with "postgresql+asyncpg" compatible with SqlAlchemy async API.
    """
    db_url = urlparse(dsn)

    try:
        assert db_url.scheme in {"postgresql", "postgres", "postgresql+asyncpg"}
    except AssertionError:
        raise ValueError(f"invalid Postgresql scheme {dsn}")

    return db_url._replace(scheme="postgresql+asyncpg").geturl()
