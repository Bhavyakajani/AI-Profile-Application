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

from fastapi import FastAPI, HTTPException
from bson import ObjectId
from pydantic import BaseModel
from profile_app.dbManager import DbManager

app = FastAPI()
db = DbManager()


@app.get("/profile")
async def get_profile_home():
    return {"message": "Hello World"}


@app.get('/profile/stats')
def get_profile_stats():
    return {'data': 'stats for profiles'}

# Because fo dynamic routing and the fact that it can detect id as string, it is better to move the function above it.
@app.get('/profile/{id}')
def get_profile_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")
    profile = db.find_by_id(pid=id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return str(profile)


# return {'profile_id': id}
@app.get('/profile/{id}/notes')
def notes_for_profile(id: str):
    return {'data': {'Strong in ServiceNow and Agile', 'Java specialist'}}
