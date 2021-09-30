import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, String, Text
from sqlalchemy.sql import expression

from fpas.db.base_model_class import Base
from fpas.db.utils import utcnow


MAX_STRING_LENGTH = 64


class Item(Base):
    name: str = Column(String(length=MAX_STRING_LENGTH), unique=True, nullable=False)
    description: Optional[str] = Column(Text)
    is_active: bool = Column(Boolean, server_default=expression.true(), nullable=False)
    created_timestamp: datetime.datetime = Column(DateTime, server_default=utcnow())

    def __repr__(self) -> str:
        return f"Item(id={self.id}, name=\"{self.name}\")"

    def __str__(self) -> str:
        return self.name
