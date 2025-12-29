"""
Database connection manager using Singleton pattern.
Handles MongoDB connection lifecycle and provides access to database and collections.
"""
import os
from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class DatabaseConnection:
    """
    Singleton class for managing MongoDB database connections.
    Ensures only one connection instance exists throughout the application.

    Behavior:
    - Reads connection info from environment variables so you can separate
      prod and test DBs easily:
        * MONGO_URI (optional): full MongoDB URI
        * MONGO_HOST (default: localhost)
        * MONGO_PORT (default: 27017)
        * MONGO_DB_NAME (default: ProfileDB)
        * MONGO_TEST_DB_NAME (default: ProfileDB_test)
        * TESTING (set to "1" to use test DB)
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
    
    def _connect(self, host: Optional[str] = None, port: Optional[int] = None, db_name: Optional[str] = None):
        """
        Establish connection to MongoDB. Values may be provided directly or via
        environment variables.
        """
        # Environment-aware defaults
        testing = os.getenv("TESTING", "0") == "1"
        host = host or os.getenv("MONGO_HOST", "localhost")
        port = port or int(os.getenv("MONGO_PORT", "27017"))

        if testing:
            db_name = db_name or os.getenv("MONGO_TEST_DB_NAME", "ProfileDB_test")
        else:
            db_name = db_name or os.getenv("MONGO_DB_NAME", "ProfileDB")

        mongo_uri = os.getenv("MONGO_URI")

        try:
            if mongo_uri:
                self._client = MongoClient(mongo_uri)
            else:
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

