import jwt
import pytest
import profile_app.authentication.security as security

def test_create_access_token():
    data = { "sub": "test@example.com" }
    assert data.items() <= jwt.decode(
        security.create_access_token(data=data), key=security.SECRET_KEY, algorithms=[security.ALGORITHM]).items()

@pytest.mark.anyio
async def test_authenticate_user():
    user = security.verify_token(
        security.create_access_token(data={"sub": "test@example.com"})
    )
    assert user.email == "test@example.com"


