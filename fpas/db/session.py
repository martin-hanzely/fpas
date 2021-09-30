from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker

from fpas.core.conf import settings
from fpas.db.utils import async_postgres_dsn


ASYNC_POSTGRES_DSN = async_postgres_dsn(settings.POSTGRES_DSN)

async_engine = create_async_engine(ASYNC_POSTGRES_DSN, echo=settings.DEBUG)

AsyncSessionLocal = sessionmaker(bind=async_engine, class_=AsyncSession, autoflush=False)
