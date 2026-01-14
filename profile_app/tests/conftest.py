import os

from profile_app.models.request_models import User
# Ensure tests use the test database - set before importing app or db_connection
os.environ["ENV_STATE"] = "test"

from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from profile_app.app import app
from profile_app.database.connection import db_connection
from profile_app.database.dependencies import get_user_repository, get_profile_repository
import profile_app.authentication.security as security

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    """Clear the test database before and after each test for isolation."""
    # Clear cached repository instances to avoid stale connections
    get_user_repository.cache_clear()
    get_profile_repository.cache_clear()
    
    # Force close any existing connection first to avoid event loop conflicts
    # This ensures we create a new connection in the test's event loop
    if db_connection._client is not None:
        try:
            await db_connection.close()
        except Exception:
            # If closing fails (e.g., different event loop), force reset
            db_connection._client = None
            db_connection._db = None
    
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
async def async_client(client, db) -> AsyncGenerator:
    """Async HTTP client backed by ASGI transport for FastAPI app.
    
    Note: The db fixture is a dependency to ensure the database connection
    is set up in the test's event loop before the async client is created.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, 
                           base_url="http://localhost:8000") as ac:
        yield ac

@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user = User(name="Test User", email="testuser@gmail.com", password="testpassword")
    await async_client.post("/user/register", json=user.model_dump())
    user_repository = get_user_repository()
    user = await user_repository.find_by_email(user.email)
    return user

@pytest.fixture()
async def registered_user_token(async_client: AsyncClient, registered_user: dict) -> str:
    response = await async_client.post("/login", data = {
        "username": registered_user["email"],
        "password": "testpassword"
    })
    return response.json()["access_token"]

@pytest.fixture()
async def registered_candidate_user(async_client: AsyncClient) -> dict:
    user = User(name="Candidate User", email="Candidate@gmail.com", password="testcandidatepassword", role="candidate")
    await async_client.post("/user/register", json=user.model_dump())
    user_repository = get_user_repository()
    user = await user_repository.find_by_email(user.email)
    return user

@pytest.fixture()
async def registered_candidate_user_token(async_client: AsyncClient, registered_candidate_user: dict) -> str:
    response = await async_client.post("/login", data = {
        "username": registered_candidate_user["email"],
        "password": "testcandidatepassword"
    })
    return response.json()["access_token"]