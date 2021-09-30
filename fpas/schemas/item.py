import datetime
from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel): ...


class ItemCreate(ItemBase):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ItemUpdate(ItemBase):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class Item(ItemBase):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_timestamp: datetime.datetime

    class Config:
        orm_mode = True
