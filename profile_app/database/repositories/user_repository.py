"""
User Repository implementing repository pattern for user operations.
"""
from typing import Optional, Dict, Any, List
from bson import ObjectId
from pymongo.collection import Collection

from profile_app.database.repositories.base_repository import BaseRepository
from profile_app.models.request_models import User


class UserRepository(BaseRepository[User]):
    """
    Repository for managing user entities.
    Provides specialized methods for user-related operations.
    """
    
    def __init__(self, collection: Collection):
        """
        Initialize UserRepository.
        
        Args:
            collection: MongoDB collection instance for users
        """
        super().__init__(collection)
    
    async def create(self, user: User | Dict[str, Any]) -> Optional[str]:
        """
        Create a new user in the database.
        
        Args:
            user: User instance or dictionary to create
            
        Returns:
            Created user ID or None if creation failed
        """
        try:
            if isinstance(user, User):
                user_dict = user.model_dump()
            else:
                user_dict = user
            
            result = await self.collection.insert_one(user_dict)
            print(f"User created with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Find a user by email address.
        
        Args:
            email: User email address
            
        Returns:
            User document or None if not found
        """
        try:
            doc = await self.collection.find_one({"email": email})
            return self._convert_objectid(doc)
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None
    
    async def exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists with the given email.
        
        Args:
            email: Email address to check
            
        Returns:
            True if user exists, False otherwise
        """
        return await self.exists({"email": email})
    
    async def search_by_name(self, name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search users by name using regex (case-insensitive).
        
        Args:
            name: Name pattern to search for
            limit: Maximum number of results to return
            
        Returns:
            List of matching user documents
        """
        try:
            regex_filter = {"$regex": name, "$options": "i"}
            cursor = self.collection.find({"name": regex_filter}).limit(limit)
            docs = await cursor.to_list(length=limit)
            return self._convert_objectid_list(docs)
        except Exception as e:
            print(f"Error searching users by name: {e}")
            return []
    
    async def update_user(self, id: str | ObjectId, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a user with new data.
        
        Args:
            id: User ID (string or ObjectId)
            user_data: Dictionary of fields to update
            
        Returns:
            Updated user document or None if not found
        """
        return await self.update(id, user_data)
    
    async def find_by_role(self, role: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Find all users with a specific role.
        
        Args:
            role: User role to filter by
            limit: Maximum number of users to return
            
        Returns:
            List of user documents
        """
        try:
            query = self.collection.find({"role": role})
            if limit:
                query = await query.to_list(length=limit)
            else:
                query = await query.to_list(length=None)
            return self._convert_objectid_list(query)
        except Exception as e:
            print(f"Error finding users by role: {e}")
            return []
        
    async def find_by_status(self, status: str = "waiting", limit: Optional[int]= None) -> List[Dict[str, Any]]:
        """
        Find users awaiting approval from Admin
        :param status: str = For Fetching Users with waiting status
        :param limit: Optional[int]: Limit the results in a single call 
        :return: List[Dict[str, Any]]: List of Users
        """
        try: 
            query = self.collection.find({"status": status})
            if limit:
                docs = await query.to_list(length=limit)
            else:
                docs = await query.to_list(length=None)
            return self._convert_objectid_list(docs)
        except Exception as e:
            print(f"Error finding users by status: {status}: {e}")
            return []

