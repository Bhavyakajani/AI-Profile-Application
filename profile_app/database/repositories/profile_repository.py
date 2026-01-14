"""
Profile Repository implementing repository pattern for profile/candidate operations.
"""
from typing import Optional, List, Dict, Any
from bson import ObjectId
from pymongo.collection import Collection

from profile_app.database.repositories.base_repository import BaseRepository
from profile_app.models.request_models import ProfileModel


class ProfileRepository(BaseRepository[ProfileModel]):
    """
    Repository for managing profile/candidate entities.
    Provides specialized methods for profile-related operations.
    """
    
    def __init__(self, collection: Collection):
        """
        Initialize ProfileRepository.
        
        Args:
            collection: MongoDB collection instance for profiles
        """
        super().__init__(collection)
    
    async def create(self, profile: ProfileModel) -> Optional[str]:
        """
        Create a new profile in the database.
        
        Args:
            profile: ProfileModel instance to create
            
        Returns:
            Created profile ID or None if creation failed
        """
        try:
            profile_dict = profile.model_dump()
            result = await self.collection.insert_one(profile_dict)
            print(f"Profile created with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating profile: {e}")
            return None
    
    async def find_by_creator(self, creator_email: str) -> Optional[Dict[str, Any]]:
        """
        Find a profile by creator email.
        
        Args:
            creator_email: Email of the profile creator
            
        Returns:
            Profile document or None if not found
        """
        try:
            doc = await self.collection.find_one({"creator": creator_email})
            return self._convert_objectid(doc)
        except Exception as e:
            print(f"Error finding profile by creator: {e}")
            return None
    
    async def exists_by_name(self, name: str) -> bool:
        """
        Check if a profile exists with the given name.
        
        Args:
            name: Profile name to check
            
        Returns:
            True if profile exists, False otherwise
        """
        return await self.exists({"name": name})

    async def exists_by_creator(self, creator_email: str) -> bool:
        """
        Check if a profile exists for the given creator.
        
        Args:
            creator_email: Creator email to check
            
        Returns:
            True if profile exists, False otherwise
        """
        return await self.exists({"creator": creator_email})

    async def search_by_name(self, name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search profiles by name using regex (case-insensitive).

        Args:
            name: Name pattern to search for
            limit: Maximum number of results to return

        Returns:
            List of matching profile documents
        """
        try:
            # Use a proper regex filter with case-insensitive option
            regex_filter = {"$regex": name, "$options": "i"}
            cursor = self.collection.find({"name": regex_filter}).limit(limit)
            docs = await cursor.to_list(length=limit)
            print(f"Found {len(docs)} profiles matching name: {name}")
            return self._convert_objectid_list(docs)
        except Exception as e:
            print(f"Error searching profiles by name: {e}")
            return []
    
    async def update_profile(self, id: str | ObjectId, profile: ProfileModel) -> Optional[Dict[str, Any]]:
        """
        Update a profile with new data.
        
        Args:
            id: Profile ID (string or ObjectId)
            profile: ProfileModel with updated data
            
        Returns:
            Updated profile document or None if not found
        """
        profile_dict = profile.model_dump()
        return await self.update(id, profile_dict)

    async def find_by_creator_email(self, creator_email: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Find all profiles created by a specific user.
        
        Args:
            creator_email: Email of the creator
            limit: Maximum number of profiles to return
            
        Returns:
            List of profile documents
        """
        try:
            query = await self.collection.find({"creator": creator_email})
            if limit:
                query = query.limit(limit)
            docs = list(query)
            return self._convert_objectid_list(docs)
        except Exception as e:
            print(f"Error finding profiles by creator: {e}")
            return []

