from __future__ import annotations

from typing import Any
from bson import ObjectId

from pymongo import MongoClient


class DbManager:
    db_name = "ProfileDB"
    collection_name = "candidates"
    client = None

    def __init__(self):

        client = None
        try:
            client = MongoClient('localhost', 27017)
            self.db = client[self.db_name]
            self.collection = self.db[self.collection_name]
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if client is None:
                client.close()
                print("Database connection closed")

    def get_db_client(self):
        return self.client

    def insert_profile(self, profile) -> Any | None:
        try:
            # Creating a dictionary with student details
            data = {
                "name": profile['name'],
                "contact_number": profile['contact_number'],
                "email": profile['email'],
                "skills": profile['skills'],
                "educations": profile['educations'],
                "work_experiences": profile['work_experiences'],
                "YoE": profile['YoE']
            }

            # Inserting the candidate data into the 'candidates' collection and obtaining the inserted ID
            pid = self.collection.insert_one(data).inserted_id
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

    def profile_exists(self, profile_json) -> bool:
        return self.collection.find_one(profile_json) is not None

    def profile_exists_by_name(self, profile_json) -> bool:
        return self.collection.find_one({"name": profile_json["name"]}) is not None

    def find_all_profiles(self):
        return self.collection.find().to_list(10)

    def update_profile(self, pid, profile):
        data = {
            "name": profile['name'],
            "contact_number": profile['contact_number'],
            "email": profile['email'],
            "skills": profile['skills'],
            "educations": profile['educations'],
            "work_experiences": profile['work_experiences'],
            "YoE": profile['YoE']
        }
        self.collection.update_one({"_id": pid}, {"$set": data})

    def delete_one(self, pid):
        if isinstance(pid, str):
            pid = ObjectId(pid)
        self.collection.delete_one({"_id": pid})
        return self.collection.delete_one({"_id": pid})
