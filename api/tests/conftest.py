import os

import pytest

os.environ["FASTAPI_CONFIG"] = "testing"  # noqa

from pytest_factoryboy import register
from src.users.factories import UserFactory
from src.tdd.factories import MemberFactory

register(UserFactory)
register(MemberFactory)


@pytest.fixture
def settings():
    from src.config import settings as _settings

    return _settings


@pytest.fixture
def app(settings):
    from src import create_app

    app = create_app()
    return app


@pytest.fixture()
def db_session(app):
    from src.database import Base, engine, SessionLocal

    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient

    yield TestClient(app)


@pytest.fixture(autouse=True)
def tmp_upload_dir(tmpdir, settings):
    settings.UPLOADS_DEFAULT_DEST = tmpdir.mkdir("tmp")
