from fastapi import Request

from settings import Settings, get_settings
from app.func_db.func_db import FuncDB


class RequestContext:
    def __init__(self, request: Request, settings: Settings):
        user = getattr(request.state, "user", None)
        self.settings = settings  # i think is better get the settings from the request.state set in the middleware
        self.request = request
        self.user = user
        self.method = request.method
        self.func_db = FuncDB(settings)


class WebSocketContext:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.func_db = FuncDB(settings)


async def get_context(request: Request) -> RequestContext:
    return RequestContext(request, get_settings())


async def get_context_websocket(request) -> WebSocketContext:
    return WebSocketContext(get_settings())
