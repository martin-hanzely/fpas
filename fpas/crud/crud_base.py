from typing import Any, Generic, Optional, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fpas.db.base_model_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    _model: Type[ModelType]

    def __init__(self, model: Type[ModelType]) -> None:
        self._model = model

    async def read(self, db: AsyncSession) -> list[ModelType]:
        result = await db.execute(select(self._model))
        return result.scalars().all()

    async def read_one(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        # Base model subclasses by default use Integer id as primary key
        result = await db.execute(select(self._model).where(self._model.id == id))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj: CreateSchemaType) -> ModelType:
        obj_dict: dict[str, Any] = jsonable_encoder(obj, exclude_unset=True)
        db_obj = self._model(**obj_dict)  # type: ignore[call-arg]
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, *, id: Any, obj: UpdateSchemaType) -> ModelType:
        cursor = await db.execute(select(self._model).where(self._model.id == id))
        # raises exception if number of results is not equal to one
        db_obj = cursor.scalar_one()
        obj_dict: dict[str, Any] = jsonable_encoder(obj, exclude_unset=True)
        for k, v in obj_dict.items():
            setattr(db_obj, k, v)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
        cursor = await db.execute(select(self._model).where(self._model.id == id))
        # raises exception if number of results is not equal to one
        db_obj = cursor.scalar_one()
        db.sync_session.delete(db_obj)  # FIXME async ORM .delete() is not working here
        await db.commit()
        return db_obj
