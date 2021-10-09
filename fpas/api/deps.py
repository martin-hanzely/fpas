from typing import AsyncGenerator

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND

from fpas import crud
from fpas.db.session import session_factory
from fpas.models.item import Item


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    try:
        db: AsyncSession = session_factory()
        yield db
    finally:
        await db.close()


async def get_item(db: AsyncSession = Depends(get_db), item_id: int = Path(None, ge=1)) -> Item:
    """
    Returns Item from given ID as path argument. Raises 404 if nothing found.
    """
    item = await crud.item.read_one(db=db, id=item_id)
    if item is None:
        raise HTTPException(HTTP_404_NOT_FOUND, "Requested Item does not exist.")
    return item
