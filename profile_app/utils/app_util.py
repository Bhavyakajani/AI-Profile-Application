from typing import Any

from bson import ObjectId
from fastapi import HTTPException

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

def hash_password(user_dict) -> dict:
    """
    Hashing the password from string to bcrypt type encryption
    Input: dict = Dictionary of User Details

    """
    user_dict["password"] = pwd_context.hash(user_dict["password"])
    return user_dict

def is_valid_objectId(id) -> HTTPException | Any:
    """
    To check if the string ID is a valid ObjectId string in DB,
    if not valid then throws a HTTPException with status code 400

    Input - id: string

    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId")

def verify_password(hashed_pwd, pwd) -> bool:
    """
    Verify if the password is correct.
    hashed_pwd: Hashed (from the passlib) password in db
    pwd: provided pwd during method call
    """
    return pwd_context.verify(pwd, hashed_pwd)

