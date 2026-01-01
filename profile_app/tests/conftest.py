import os
# Ensure tests use the test database - set before importing app or db_connection
os.environ["ENV_STATE"] = "test"

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
    # Ensure the async client is created in the event loop running the tests
    await db_connection._connect()
    database = db_connection.get_database()
    # Drop database before test
    await database.client.drop_database(database.name)
    try:
        yield
    finally:
        # Drop database after test and close connection
        await database.client.drop_database(database.name)
        await db_connection.close()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    """Async HTTP client backed by ASGI transport for FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, 
                           base_url="http://localhost:8000") as ac:
        yield ac

