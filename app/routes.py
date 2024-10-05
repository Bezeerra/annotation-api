from fastapi import FastAPI

from settings import Settings
from app.users import router as user_router
from app.chat import router as chat_router
from app.annotations import router as annotation_router


def set_prefix_routes(app: FastAPI, settings: Settings):
    v = 'api/' + settings.API_VERSION
    app.include_router(user_router, prefix=f"/{v}/users", tags=["users"])
    app.include_router(chat_router, prefix=f"/{v}/chat", tags=["chat"])
    app.include_router(annotation_router, prefix=f"/{v}/annotations", tags=["annotations"])
