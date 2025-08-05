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

from bson import ObjectId
from fastapi import FastAPI, HTTPException, status, Response
from passlib.context import CryptContext

from profile_app.dbManager import profile_db, user_db
from profile_app.hashing import hash_password
from profile_app.models import ProfileModel, ShowProfile, User, ShowUser, UpdateUserResponse
from profile_app.routers import profile, user

app = FastAPI()
"""Running on port 8001 by --port 8001"""



app.include_router(profile.router)
app.include_router(user.router)




