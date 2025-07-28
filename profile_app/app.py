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
from typing import Optional
from fastapi import FastAPI, HTTPException, Body, status, Response
from bson import ObjectId
from profile_app.dbManager import DbManager
from profile_app.Profile import ProfileModel, ProfilesCollection

app = FastAPI()
"""Running on port 8001 by --port 8001"""

db = DbManager()


@app.get("/profile_query_params")
def index(limit: Optional[int] = 10, has_notes: Optional[bool] = False, sort: Optional[str] = None):
    if has_notes:
        return {"message": f"{limit} Profiles with notes"}
    else:
        return{"data": f"{limit} Profiles without notes"}


@app.get("/profiles")
def get_all_profiles():
    profiles = db.find_all_profiles()
    return ProfilesCollection(profiles = profiles)

@app.post('/parse', response_model=ProfileModel, status_code=status.HTTP_201_CREATED)
def create_profile(profile: ProfileModel):
    if profile is None:
        raise HTTPException(status_code=402, detail='Bad Request: Invalid Profile Details')
    pid = db.insert_profile(profile.model_dump())
    if pid:
        return {"profile_id": pid}
    else:
        raise HTTPException(status_code=400)

@app.get('/profile/stats')
def get_profile_stats():
    return {'data': 'stats for profiles'}
# Because fo dynamic routing and the fact that it can detect id as string, it is better to move the function above it.


@app.delete('/profile/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_profile_by_id(id,response: Response):
    if not ObjectId.is_valid(id):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    delete_result = db.delete_one(id)
    if delete_result.deleted_count == 1:
        return Response(status_code=204)
    raise HTTPException(status_code=404, detail=f"Profile {id} not found")

@app.patch('/profile/{id}', status_code=202)
def update_profile(id, response: Response):
    if not ObjectId.is_valid(id):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Invalid ObjectId")


@app.get('/profile/{id}', status_code=200)
def get_profile_by_id(id: str, response: Response):
    if not ObjectId.is_valid(id):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    profile = db.find_by_id(pid=id)
    if profile is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=404, detail=f"Profile with id: {id} not found")
    return str(profile)
# return {'profile_id': id}

@app.get('/profile/{id}/notes')
def notes_for_profile(id: str):
    return {'data': {'Strong in ServiceNow and Agile', 'Java specialist'}}

