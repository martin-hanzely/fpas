from fastapi import APIRouter
from pydantic import BaseModel

from fpas.core.conf import settings


router = APIRouter()


class RootResponseMessage(BaseModel):
    project_name: str = settings.PROJECT_NAME
    version: str = settings.VERSION


@router.get("/", response_model=RootResponseMessage)
async def root():
    return RootResponseMessage()
