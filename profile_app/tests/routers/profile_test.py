import pytest

from httpx import AsyncClient

from profile_app.models.request_models import ProfileCreateRequest, ProfileModel

@pytest.fixture()
async def get_all_profiles(async_client: AsyncClient):
    """Helper to get all profiles via the API and return the list of profiles."""
    response = await async_client.get("/profile/")
    return response

@pytest.mark.anyio
async def test_get_all_profiles(get_all_profiles):
    response = get_all_profiles
    assert response.status_code == 200