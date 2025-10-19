"""
CS 340 – MongoDB CRUD Module
Author: Justin Hartwick
Description:
    Handles all Create, Read, Update, and Delete operations
    for the AAC Animal Shelter database used in the Grazioso Salvare
    dashboard project.
"""

# -------------------------------------------------
# Imports
# -------------------------------------------------
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Any, Dict, List


class AnimalShelter:
    """
    CRUD operations for the AAC Animal Shelter database.
    This class manages the MongoDB connection and provides
    methods to create, read, update, and delete records
    in the 'animals' collection.
    """

    def __init__(
        self,
        username: str,
        password: str,
        host: str = "127.0.0.1",
        port: int = 27017,
        db_name: str = "aac",
        collection_name: str = "animals",
        **client_kwargs: Any
    ) -> None:
        """
        Initialize the connection to MongoDB.
        Requires valid username and password credentials.
        """

        if not username or not password:
            raise ValueError("Username and password are required for MongoDB connection.")

        # Build the connection URI (authSource must match lowercase 'aac')
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource=aac"

        # Set a connection timeout (default 5 seconds)
        client_kwargs.setdefault("serverSelectionTimeoutMS", 5000)

        try:
            # Connect to MongoDB and select database/collection
            self._client = MongoClient(uri, **client_kwargs)
            self._db = self._client[db_name]
            self._col = self._db[collection_name]

            # Test the connection
            self._client.admin.command("ping")
            print("✅ Connected to MongoDB successfully.")
        except PyMongoError as e:
            raise ConnectionError(f"❌ MongoDB connection failed: {e}")

    # -------------------------------------------------
    # Create
    # -------------------------------------------------
    def create(self, data: Dict[str, Any]) -> bool:
        """
        Insert a single document into the collection.
        Returns True if successful, otherwise False.
        """
        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary.")

        try:
            result = self._col.insert_one(data)
            return result.acknowledged
        except PyMongoError as e:
            print(f"Error inserting document: {e}")
            return False

    # -------------------------------------------------
    # Read
    # -------------------------------------------------
    def read(
        self,
        query: Dict[str, Any],
        projection: Dict[str, Any] = None,
        limit: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Read documents that match the query.
        Returns a list of matching documents.
        """
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary.")

        try:
            cursor = self._col.find(query, projection)
            if limit > 0:
                cursor = cursor.limit(limit)
            return list(cursor)
        except PyMongoError as e:
            print(f"Error reading from database: {e}")
            return []

    # -------------------------------------------------
    # Update
    # -------------------------------------------------
    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Update all documents matching the query with new data.
        Returns the number of modified documents.
        """
        if not query or not update_data:
            raise ValueError("Both query and update data must be provided.")

        try:
            result = self._col.update_many(query, {"$set": update_data})
            return result.modified_count
        except PyMongoError as e:
            print(f"Error updating documents: {e}")
            return 0

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------
    def delete(self, query: Dict[str, Any]) -> int:
        """
        Delete all documents matching the query.
        Returns the number of deleted documents.
        """
        if not query:
            raise ValueError("Delete query cannot be empty.")

        try:
            result = self._col.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Error deleting documents: {e}")
            return 0

    # -------------------------------------------------
    # Ping
    # -------------------------------------------------
    def ping(self) -> dict:
        """
        Ping the MongoDB server to verify connectivity.
        Returns a dictionary if successful.
        """
        try:
            return self._client.admin.command("ping")
        except PyMongoError as e:
            print(f"Ping failed: {e}")
            return {}
