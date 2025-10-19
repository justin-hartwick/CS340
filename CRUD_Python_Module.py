"""
CS 340 – MongoDB CRUD Module
Author: Justin Hartwick
Description: Handles all Create, Read, Update, and Delete operations
for the AAC Animal Shelter database used in the Dash dashboard project.
"""

# ------------------------------
# Imports
# ------------------------------
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Any, Dict, List


class AnimalShelter:
    """
    CRUD operations class for the AAC Animal Shelter database.
    This class manages the connection and allows Create, Read, Update,
    and Delete actions for the 'animals' collection.
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
        Initialize the connection to MongoDB using authentication.
        """
        if not username or not password:
            raise ValueError("Both username and password are required for connection.")

        # Connect directly to the AAC database with authSource=aac (required by rubric)
        uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource=aac"

        client_kwargs.setdefault("serverSelectionTimeoutMS", 5000)

        # Create the MongoDB client and set up the database and collection
        self._client = MongoClient(uri, **client_kwargs)
        self._db = self._client[db_name]
        self._col = self._db[collection_name]

        # Test connection early to surface any auth errors immediately
        try:
            self._client.admin.command("ping")
        except PyMongoError as e:
            raise ConnectionError(f"Unable to connect to MongoDB: {e}")

    # ------------------------------
    # Create
    # ------------------------------
    def create(self, data: Dict[str, Any]) -> bool:
        """
        Insert a single document into the collection.
        Returns True if acknowledged, otherwise False.
        """
        if not data or not isinstance(data, dict):
            raise ValueError("Data must be a non-empty dictionary.")

        try:
            result = self._col.insert_one(data)
            return result.acknowledged
        except PyMongoError as e:
            print(f"Error inserting document: {e}")
            return False

    # ------------------------------
    # Read
    # ------------------------------
    def read(
        self,
        query: Dict[str, Any],
        projection: Dict[str, Any] = None,
        limit: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Read and return documents that match the given query.
        """
        if not isinstance(query, dict):
            raise ValueError("Query must be provided as a dictionary.")

        try:
            cursor = self._col.find(query, projection)
            if limit > 0:
                cursor = cursor.limit(limit)
            return list(cursor)
        except PyMongoError as e:
            print(f"Error reading from database: {e}")
            return []

    # ------------------------------
    # Update
    # ------------------------------
    def update(self, query: Dict[str, Any], update_data: Dict[str, Any]) -> int:
        """
        Update documents matching the query with the provided fields.
        Returns the number of modified documents.
        """
        if not query or not update_data:
            raise ValueError("Both query and update data are required.")

        try:
            result = self._col.update_many(query, {"$set": update_data})
            return result.modified_count
        except PyMongoError as e:
            print(f"Error updating document(s): {e}")
            return 0

    # ------------------------------
    # Delete
    # ------------------------------
    def delete(self, query: Dict[str, Any]) -> int:
        """
        Delete documents matching the query.
        Returns the number of deleted documents.
        """
        if not query:
            raise ValueError("Delete query cannot be empty.")

        try:
            result = self._col.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Error deleting document(s): {e}")
            return 0

    # ------------------------------
    # Ping
    # ------------------------------
    def ping(self) -> dict:
        """
        Ping the database to confirm an active connection.
        Returns the response dictionary if successful.
        """
        try:
            return self._client.admin.command("ping")
        except PyMongoError as e:
            print(f"Ping failed: {e}")
            return {}
