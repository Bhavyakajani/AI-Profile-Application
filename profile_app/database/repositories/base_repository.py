"""
Base repository interface defining the contract for all repositories.
Follows Repository Pattern for clean separation of data access logic.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Dict, Any
from bson import ObjectId
from pymongo.collection import Collection
import logging

T = TypeVar('T')  # Entity type

logger = logging.getLogger(__name__)
class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository defining common CRUD operations.
    All specific repositories should inherit from this class.
    """
    
    def __init__(self, collection: Collection):
        """
        Initialize repository with a MongoDB collection.
        
        Args:
            collection: MongoDB collection instance
        """
        self.collection = collection
    
    def _convert_objectid(self, doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Convert ObjectId to string in document.
        
        Args:
            doc: Document dictionary
            
        Returns:
            Document with ObjectId converted to string
        """
        if doc and "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
        return doc
    
    def _convert_objectid_list(self, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convert ObjectId to string in a list of documents.
        
        Args:
            docs: List of document dictionaries
            
        Returns:
            List of documents with ObjectId converted to string
        """
        return [self._convert_objectid(doc) for doc in docs if doc]
    
    def _to_objectid(self, id: str | ObjectId) -> ObjectId:
        """
        Convert string ID to ObjectId.
        
        Args:
            id: String or ObjectId
            
        Returns:
            ObjectId instance
        """
        if isinstance(id, str):
            return ObjectId(id)
        return id
    
    @abstractmethod
    async def create(self, entity: T) -> Optional[str]:
        """
        Create a new entity in the database.
        
        Args:
            entity: Entity to create
            
        Returns:
            Created entity ID or None if creation failed
        """
        pass
    
    async def find_by_id(self, id: str | ObjectId) -> Optional[Dict[str, Any]]:
        """
        Find an entity by its ID.
        
        Args:
            id: Entity ID (string or ObjectId)
            
        Returns:
            Entity document or None if not found
        """
        try:
            oid = self._to_objectid(id)
            doc = await self.collection.find_one({"_id": oid})
            return self._convert_objectid(doc)
        except Exception as e:
            print(f"Error finding entity by ID: {e}")
            return None
    
    async def find_all(self, limit: Optional[int] = None, skip: int = 0) -> List[Dict[str, Any]]:
        """
        Find all entities in the collection.
        
        Args:
            limit: Maximum number of documents to return
            skip: Number of documents to skip
            
        Returns:
            List of entity documents
        """
        try:
            query = self.collection.find().skip(skip)
            
            if limit:
                query = await query.limit(limit).to_list(length=limit)
            else:
                docs = [doc async for doc in query]
            return self._convert_objectid_list(docs)
        except Exception as e:
            logger.exception(f"Error finding all entities: {e}")
            return []
    
    async def count(self) -> int:
        """
        Count total number of entities in the collection.
        
        Returns:
            Total count of entities
        """
        try:
            return await self.collection.estimated_document_count()
        except Exception as e:
            print(f"Error counting entities: {e}")
            return 0
    
    async def update(self, id: str | ObjectId, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an entity by ID.
        
        Args:
            id: Entity ID (string or ObjectId)
            update_data: Dictionary of fields to update
            
        Returns:
            Updated entity document or None if not found
        """
        try:
            oid = self._to_objectid(id)
            from pymongo import ReturnDocument
            result = await self.collection.find_one_and_update(
                {"_id": oid},
                {"$set": update_data},
                return_document=ReturnDocument.AFTER
            )
            return self._convert_objectid(result)
        except Exception as e:
            print(f"Error updating entity: {e}")
            return None
    
    async def delete(self, id: str | ObjectId) -> bool:
        """
        Delete an entity by ID.
        
        Args:
            id: Entity ID (string or ObjectId)
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            oid = self._to_objectid(id)
            result = await self.collection.delete_one({"_id": oid})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting entity: {e}")
            return False
    
    async def exists(self, filter: Dict[str, Any]) -> bool:
        """
        Check if an entity exists matching the filter.
        
        Args:
            filter: MongoDB filter dictionary
            
        Returns:
            True if entity exists, False otherwise
        """
        print("exists filter:", filter)
        try:
            res = await self.collection.find_one(filter) is not None
            print("exists result:", res)
            return res
        except Exception as e:
            print(f"Error checking entity existence: {e}")
            return False

