"""
Dependency injection for repositories.
Provides repository instances to FastAPI routes using dependency injection.
"""
from functools import lru_cache

from profile_app.database.connection import db_connection
from profile_app.database.repositories import ProfileRepository, UserRepository


@lru_cache()
def get_profile_repository() -> ProfileRepository:
    """
    Get ProfileRepository instance (singleton via lru_cache).
    
    Returns:
        ProfileRepository instance
    """
    collection = db_connection.get_collection("candidates")
    return ProfileRepository(collection)


@lru_cache()
def get_user_repository() -> UserRepository:
    """
    Get UserRepository instance (singleton via lru_cache).
    
    Returns:
        UserRepository instance
    """
    collection = db_connection.get_collection("users")
    return UserRepository(collection)

