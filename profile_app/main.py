import llm_model as llm
from profile_app.database import dbManager as db
import os


def main():
    database = db.DbManager("candidates")
    folder_path = "./data"

    for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}")

            profile_json = llm.extract_with_llm(file_path)
            if database.profile_exists_by_name(profile_json):
                print(f"{profile_json["name"]} already exists")
            else:
                pid = database.insert_profile(profile_json)
                print(f"Inserted profile with ID: {pid}")


if __name__ == "__main__":
    main()

