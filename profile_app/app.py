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
from pydantic import BaseModel

app = FastAPI()


class UserPostIn(BaseModel):
    body: str


class UserPost(UserPostIn):
    id: int


post_table = {}


@app.post("/post", response_model=UserPost)
async def create_post(post: UserPost):
    # Convert the received post into dictionary to access the data
    data = post.model_dump(dict)
    # To populate the id based on the number of records in the post_table dictionary
    id = len(post_table)
    # Post new id
    new_post = {**data, "id": id}
    # Fill the data in the dictionary with 'id'
    post_table[id] = new_post
    return new_post


@app.get("/")
async def root():
    return {"message": "Hello World"}
