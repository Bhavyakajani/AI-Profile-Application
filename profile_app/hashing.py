from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

def hash_password(user_dict):
    user_dict["password"] = pwd_context.hash(user_dict["password"])
    return user_dict