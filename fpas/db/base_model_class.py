from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped


@as_declarative()
class Base:

    @declared_attr
    def __tablename__(cls) -> Mapped[str]:
        return cls.__name__.lower()

    id: int = Column(Integer, primary_key=True)  # use Integer id as primary key by default
