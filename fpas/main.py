from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from fpas.api.routers.api import router as api_router
from fpas.core.conf import settings


def get_app() -> FastAPI:
    app = FastAPI(debug=settings.DEBUG, title=settings.PROJECT_NAME)

    if settings.BACKEND_CORS_ORIGINS:  # pragma: no cover
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router)
    return app


app = get_app()
