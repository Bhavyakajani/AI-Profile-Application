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

from fastapi import FastAPI
from profile_app.routers import profile, user, auth

app = FastAPI()
"""Running on port 8001 by --port 8001"""

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(user.router)
