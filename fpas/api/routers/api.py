from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from fpas.api.routers.items import router as items_router
from fpas.core.conf import settings


class RootResponseMessage(BaseModel):
    project_name: str = settings.PROJECT_NAME
    version: str = settings.VERSION


router = APIRouter()


@router.get("/", response_model=RootResponseMessage)
async def root() -> Any:
    return RootResponseMessage()


router.include_router(items_router, prefix="/items", tags=["items"])
