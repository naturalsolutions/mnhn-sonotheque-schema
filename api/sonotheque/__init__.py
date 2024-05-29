import os
from contextlib import asynccontextmanager
from broadcaster import Broadcast
from fastapi import FastAPI, Request

from sonotheque.config import settings

broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, root_path=os.environ.get("API_ROOT_PATH", "/api/v1"))

    from sonotheque.logging import configure_logging
    configure_logging()

    # do this before loading routes
    from sonotheque.celery_utils import create_celery
    app.celery_app = create_celery()

    from sonotheque.users import users_router
    app.include_router(users_router)

    from sonotheque.tdd import tdd_router
    app.include_router(tdd_router)

    from sonotheque.ws import ws_router
    app.include_router(ws_router)

    from sonotheque.ws.views import register_socketio_app
    register_socketio_app(app)

    @app.get("/")
    async def root(request: Request):
        return {"message": "Hello World", "root_path": request.scope.get("root_path")}

    return app
