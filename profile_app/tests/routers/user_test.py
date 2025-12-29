import pytest

from httpx import AsyncClient

from profile_app.models.request_models import User

async def create_user(body: User | dict, async_client: AsyncClient):
    """Helper to create a user via the API and return the raw response."""
    body_data = body.model_dump() if hasattr(body, "model_dump") else body
    response = await async_client.post("/user/", json=body_data)
    return response


@pytest.fixture()
async def created_user(async_client: AsyncClient):
    """Create a user and return the HTTP response."""
    user = User(name="test", email="test@example.com", password="testpassword", role="user")
    response = await create_user(body=user, async_client=async_client)
    return response

@pytest.fixture()
async def created_user_no_body(async_client: AsyncClient):
    response = await create_user(body={}, async_client=async_client)
    return response

@pytest.fixture()
async def deleted_user(created_user, async_client: AsyncClient):
    user_id = created_user.json()["id"]
    response = await async_client.delete(f"/user/{user_id}")
    return response

@pytest.mark.anyio
async def test_create_user(created_user):
    resp = created_user
    data = resp.json()

    assert resp.status_code == 200
    assert "id" in data
    assert data["name"] == "test"
    assert data["email"] == "test@example.com"
    assert data["role"] == "user"
    assert isinstance(data["id"], str)

@pytest.mark.anyio
async def test_create_user_no_body(created_user_no_body):
    resp = created_user_no_body
    assert resp.status_code == 422

# @pytest.mark.anyio
# async def test_delete_user(deleted_user):
#     resp = deleted_user
#     assert resp.status_code == 204