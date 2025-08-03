# --------Flask API ----------------------
# from flask import Flask, render_template
#
#
# app = Flask(__name__)
#
# @app.route('/')
# def index():
#     return "Hello World!"
# -----------FAST API-----------------------
from typing import List
from fastapi import FastAPI, HTTPException, Body, status, Response
from bson import ObjectId
from profile_app.dbManager import DbManager
from profile_app.Profile import ProfileModel, ShowProfile, User, ShowUser, UpdateUserResponse
from passlib.context import CryptContext
from profile_app.hashing import hash_password

app = FastAPI()
"""Running on port 8001 by --port 8001"""

profile_db = DbManager("candidates")
user_db = DbManager("users")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")



@app.get("/profiles", response_model=List[ShowProfile], tags=['Profiles'])
def get_all_profiles():
    profiles = profile_db.find_all_profiles()
    return profiles

@app.post('/parse', response_model=ProfileModel, status_code=status.HTTP_201_CREATED, tags=['Profiles'])
def create_profile(profile: ProfileModel):
    if profile is None:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')
    pid = profile_db.insert_profile(profile)
    if pid:
        return {"profile_id": pid}
    else:
        raise HTTPException(status_code=400)


# Because fo dynamic routing and the fact that it can detect id as string, it is better to move the function above it.


@app.delete('/profile/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Profiles'])
def delete_profile_by_id(id, response: Response):
    if not ObjectId.is_valid(id):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    delete_result = profile_db.delete_one(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")


@app.patch('/profile/{id}', status_code=202, tags=['Profiles'])
def update_profile(id: str, profile: ProfileModel):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

    update_result = profile_db.update_profile(ObjectId(id), profile)

    if update_result:
        update_result["_id"] = str(update_result["_id"])
        return {"message": f"Profile {id} updated successfully", "updated_data": update_result}
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@app.get('/profile/{id}', status_code=200, response_model=ShowProfile, tags=['Profiles'])
def get_profile_by_id(id: str, response: Response):
    if not ObjectId.is_valid(id):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    profile = profile_db.find_by_id(pid=id)
    if profile is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with id: {id} not found")
    return profile

@app.post('/user', response_model=ShowUser, tags=['Users'])
def create_user(user: User):
    if user:
        user_dict = user.model_dump()
        user_dict = hash_password(user_dict)
        new_user = user_db.insert_user(user_dict)
        return ShowUser(name = user.name, email=user.email)
    else:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')


@app.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Users'])
def delete_user(id, response: Response):
    if not ObjectId.is_valid(id):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    delete_result = user_db.delete_one(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@app.get('/user/{id}', status_code=status.HTTP_200_OK, response_model=ShowUser, tags=['Users'])
def get_user(id):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid User Id")
    user = user_db.find_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return ShowUser(name=user["name"], email=user["email"])

@app.patch('/user/{id}', response_model=UpdateUserResponse, tags=['Users'])
def update_user(id, user: User):
    oid_user = ObjectId(id)
    if not oid_user.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid User Id")
    user_dict = hash_password(user.model_dump())
    new_user = user_db.update_user(oid_user, user_dict)

    if new_user:
        new_user["_id"] = str(new_user["_id"])
        return UpdateUserResponse(message = f"User {id} updated successfully", updated_data = new_user)
    else:
        raise HTTPException(status_code=404, detail=f"Profile {id} not found")




