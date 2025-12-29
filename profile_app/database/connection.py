"""
Database connection manager using Singleton pattern.
Handles MongoDB connection lifecycle and provides access to database and collections.
"""
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class DatabaseConnection:
    """
    Singleton class for managing MongoDB database connections.
    Ensures only one connection instance exists throughout the application.
    """
    _instance: Optional['DatabaseConnection'] = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._connect()
    
    def _connect(self, host: str = 'localhost', port: int = 27017, db_name: str = 'ProfileDB'):
        """
        Establish connection to MongoDB.
        
        Args:
            host: MongoDB host address
            port: MongoDB port number
            db_name: Database name
        """
        try:
            self._client = MongoClient(host, port)
            self._db = self._client[db_name]
            print(f"Connected to MongoDB database: {db_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise
    
    def get_database(self) -> Database:
        """
        Get the database instance.
        
        Returns:
            Database: MongoDB database instance
        """
        if self._db is None:
            raise RuntimeError("Database connection not established")
        return self._db
    
    def get_collection(self, collection_name: str) -> Collection:
        """
        Get a collection from the database.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection: MongoDB collection instance
        """
        db = self.get_database()
        return db[collection_name]
    
    def close(self):
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("Database connection closed")
    
    def __del__(self):
        """Cleanup on object destruction."""
        self.close()


# Global database connection instance
db_connection = DatabaseConnection()

