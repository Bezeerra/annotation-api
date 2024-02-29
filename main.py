from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.midlle import setup_middleware, register_middleware
from app.routes import set_prefix_routes
from settings import get_settings, Settings


def create_app(settings: Settings):

    @asynccontextmanager
    async def app_lifespan(app: FastAPI):
        yield

    app = (
        FastAPI(lifespan=app_lifespan)
        if settings.debug_mode
        else FastAPI(docs_url=None, redoc_url=None, openapi_url=None, lifespan=app_lifespan)
    )

    register_middleware(app, settings)
    set_prefix_routes(app, settings)
    return app, settings


app, settings = create_app(get_settings())
