from sqlalchemy.sql import functions
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime


class utcnow(functions.FunctionElement):
    type = DateTime  # type: ignore[assignment]


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
