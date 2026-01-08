import json
import pytest

from httpx import AsyncClient

from profile_app.models.request_models import ProfileModel
from profile_app.models.sub_models import Education, WorkExperience
from profile_app.tests.conftest import async_client, registered_user, registered_user_token

test_profile = ProfileModel(
    name="Test Profile",
    contact_number="1234567890",
    email="test@example.com",
    skills=["Python", "FastAPI"],
    educations=[Education(
        institution="Test School",
        degree="Test Degree",
        start_date="2020-01-01",
        end_date="2024-01-01")],
    work_experiences=[WorkExperience(
        company="Test Company",
        role="Test Title",
        start_date="2020-01-01",
        end_date="2024-01-01")],
    YoE="4"
)

@pytest.fixture()
async def get_all_profiles(async_client: AsyncClient):
    """Helper to get all profiles via the API and return the list of profiles."""
    response = await async_client.get("/profile/")
    return response

async def create_profile(profile_body: ProfileModel, async_client: AsyncClient, registered_user_token: str) -> dict:
    response = await async_client.post(
        "/profile/",
        json=profile_body.model_dump(),
        headers={"Authorization": f"Bearer {registered_user_token}"},
    )
    return response.json()

@pytest.fixture()
async def created_profile(async_client: AsyncClient, registered_user_token: str):
    return await create_profile(profile_body=test_profile, async_client=async_client, registered_user_token=registered_user_token)

@pytest.mark.anyio
async def test_get_all_profiles(get_all_profiles):
    response = get_all_profiles
    assert response.status_code == 200

@pytest.mark.anyio
async def test_create_profile(async_client: AsyncClient, registered_user_token: str, registered_user: dict):
    profile_body = test_profile.model_dump()

    response = await async_client.post(
        "/profile/",
        json=profile_body, 
        headers={"Authorization": f"Bearer {registered_user_token}"}
    )

    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    # Check that all test profile fields are present in response (excluding id/creator which are added by the API)
    
    for key, value in profile_body.items():
        if key not in ["creator"]:  # creator is added by the API
            assert key in response_data
            assert response_data[key] == value
        
        assert response_data["creator"] == registered_user["email"]