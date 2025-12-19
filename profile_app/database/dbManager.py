from __future__ import annotations

from typing import Any, Mapping
from bson import ObjectId

from pymongo import MongoClient, ReturnDocument

from profile_app.models.request_models import ProfileModel


class DbManager:
    db_name = "ProfileDB"
    client = None

    def __init__(self, collection_name):

        client = None
        try:
            client = MongoClient('localhost', 27017)
            self.db = client[self.db_name]
            self.collection = self.db[collection_name]
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if client is None:
                client.close()
                print("Database connection closed")

    def get_db_client(self):
        return self.client

    def get_db(self):
        return self.collection

    def insert_profile(self, profile: ProfileModel) -> Any | None:
        try:
            # Inserting the candidate data into the 'candidates' collection and getting the inserted ID
            pid = self.collection.insert_one(profile.model_dump()).inserted_id
            # Printing a message indicating the successful insertion of data with the obtained ID
            print(f"Data inserted with ID: {pid}")
            return pid
        except Exception as e:
            # Handling exceptions and printing an error message if data insertion fails
            print(f"Error: {e}")

    def find_by_id(self, pid):
        if isinstance(pid, str):
            pid = ObjectId(pid)
        return self.collection.find_one({"_id": pid})

    def find_by_key(self, profile_json) -> dict:
        return self.collection.find_one({"creator": profile_json["creator"]})

    def profile_exists(self, profile_json) -> bool:
        return self.collection.find_one(profile_json) is not None

    def profile_exists_by_name(self, profile_json) -> bool:
        return self.collection.find_one({"name": profile_json["name"]}) is not None

    def find_all_profiles(self):
        docs = self.collection.find().to_list(10)
        return [self.convert_objectid(doc) for doc in docs]

    def count_all_documents_in_collection(self):
        return self.collection.estimated_document_count()

    def update_profile(self, pid, profile: ProfileModel) -> dict :
        return self.collection.find_one_and_update({"_id": pid}, {"$set": profile.model_dump()}, return_document=ReturnDocument.AFTER)

    def delete_one(self, pid):
        if isinstance(pid, str):
            pid = ObjectId(pid)
        return self.collection.delete_one({"_id": pid})

    def insert_user(self, data: dict) -> Any | Exception |None:
        print(data["password"])
        try:
            result = self.collection.insert_one(data)
            uid = result.inserted_id
            print(f"User created with ID: {uid}")
            return uid
        except Exception as e:
            print(f"Insert error: {e}")

    def update_user(self, oid_user, user) -> dict :
        return self.collection.find_one_and_update(
            {"_id": oid_user}, {"$set": user}, return_document=ReturnDocument.AFTER
        )
    
    async def search_user_by_name(self, name: str) -> dict | None:
        regex = {"$regex": name, "$options": "i"}
        results = await self.collection.find({"name": regex}).to_list(10)
        return results

    def convert_objectid(self, doc: dict) -> dict | Mapping[str, Any]:
        if "_id" in doc and isinstance(doc["_id"], ObjectId):
            doc["_id"] = str(doc["_id"])
        return doc

profile_db = DbManager("candidates")
user_db = DbManager("users")