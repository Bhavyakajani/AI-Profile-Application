import os
# Ensure tests use the test database - set before importing app or db_connection
os.environ.setdefault("TESTING", "1")
os.environ.setdefault("MONGO_TEST_DB_NAME", "ProfileDB_test")

from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from profile_app.app import app
from profile_app.database.connection import db_connection

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    """Clear the test database before and after each test for isolation."""
    database = db_connection.get_database()
    # Drop database before test
    database.client.drop_database(database.name)
    try:
        yield
    finally:
        # Drop database after test
        database.client.drop_database(database.name)


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    """Async HTTP client backed by ASGI transport for FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, 
                           base_url="http://localhost:8000") as ac:
        yield ac

