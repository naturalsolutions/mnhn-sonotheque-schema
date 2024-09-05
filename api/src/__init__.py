# import os
from contextlib import asynccontextmanager
from broadcaster import Broadcast
from fastapi import FastAPI, Request

from src.config import settings

broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, root_path="/")

    from src.logging import configure_logging

    configure_logging()

    # do this before loading routes
    from src.celery_utils import create_celery

    app.celery_app = create_celery()

    from src.models import (
        datasets,  # noqa
        medias,  # noqa
        media_files,  # noqa
        organizations,  # noqa
        people,  # noqa
        devices,  # noqa
        sampling_events,  # noqa
        locations,  # noqa
        occurences,  # noqa
        taxa,  # noqa
        identifications,  # noqa
        acoustic_events,  # noqa
        # captures_rel,  # noqa
    )
    from src.models.associations import captures_rel  # noqa

    from src.routers.import_tasks import router as import_tasks_router

    app.include_router(import_tasks_router)

    # from src.users import users_router

    # app.include_router(users_router)

    # from src.tdd import tdd_router

    # app.include_router(tdd_router)

    # from src.ws import ws_router

    # app.include_router(ws_router)

    # from src.ws.views import register_socketio_app

    # register_socketio_app(app)

    @app.get("/")
    async def root(request: Request):
        return {"message": "Hello World", "root_path": request.scope.get("root_path")}

    return app
