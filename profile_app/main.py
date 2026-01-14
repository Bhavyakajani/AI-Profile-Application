from profile_app.ai import llm_model as llm
from profile_app.database.connection import db_connection
from profile_app.database.repositories import ProfileRepository
from profile_app.models.request_models import ProfileModel
import os


def main():
    # Get profile repository using the new repository pattern
    collection = db_connection.get_collection("candidates")
    profile_repo = ProfileRepository(collection)
    
    folder_path = "./data"

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing {filename}")

        profile_json = llm.extract_with_llm(file_path)
        profile_name = profile_json.get("name", "")
        
        if profile_repo.exists_by_name(profile_name):
            print(f"{profile_name} already exists")
        else:
            profile_model = ProfileModel(**profile_json)
            pid = profile_repo.create(profile_model)
            if pid:
                print(f"Inserted profile with ID: {pid}")
            else:
                print(f"Failed to insert profile: {profile_name}")


if __name__ == "__main__":
    main()

