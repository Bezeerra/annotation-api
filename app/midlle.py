
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from settings import Settings


origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    r"^http://127.0.0.1:.*",
    r"^http://localhost:.*",
    r"^ws://.*"
    r"ws.*"
    r".*",
]


def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_middleware(app: FastAPI, settings: Settings):
    setup_middleware(app)

    @app.middleware("http")
    async def authorize_request(request: Request | WebSocket, call_next):
        request.state.settings = settings
        response = await call_next(request)
        return response
