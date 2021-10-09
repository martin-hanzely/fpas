from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from fpas import crud, schemas
from fpas.api import deps
from fpas.models.item import Item


router = APIRouter()


@router.get("/", response_model=list[schemas.Item])
async def read(*, db: AsyncSession = Depends(deps.get_db)) -> Any:
    items = await crud.item.read(db=db)
    return items


@router.get("/{id}", response_model=schemas.Item)
async def read_one(*, item: Item = Depends(deps.get_item)) -> Any:
    return item


@router.post("/", response_model=schemas.Item)
async def create(*, db: AsyncSession = Depends(deps.get_db), obj: schemas.ItemCreate) -> Any:
    try:
        return await crud.item.create(db=db, obj=obj)
    except IntegrityError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, e)


@router.put("/{id}", response_model=schemas.Item)
async def update(
    *,
    db: AsyncSession = Depends(deps.get_db),
    item: Item = Depends(deps.get_item),
    obj: schemas.ItemUpdate
) -> Any:
    try:
        return await crud.item.update(db=db, id=item.id, obj=obj)
    except IntegrityError as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, e)


@router.delete("/{id}", response_model=schemas.Item)
async def delete(
    *, db: AsyncSession = Depends(deps.get_db), item: Item = Depends(deps.get_item)
) -> Any:
    return await crud.item.delete(db=db, id=item.id)
