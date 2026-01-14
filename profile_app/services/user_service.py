from profile_app.models.request_models import User
from profile_app.models.response_models import UserRoleResponse


class UserService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        pass 

    def is_user_admin(self, current_user: dict[any, any]) -> bool:
        return current_user["role"] == "admin"
    
    def is_user_candidate(self, current_user: dict[any, any]) -> bool:
        return current_user["role"] == "candidate"
    
    def is_user_client(self, current_user: dict[any, any]) -> bool:
        return current_user["role"] == "client"
    
    def is_status_waiting(self, user: dict[any, any]) -> bool:
        return user["status"] == "waiting"
    
    def get_user_role_status_model(user: User) -> UserRoleResponse:
        return UserRoleResponse(
        id=str(user["_id"]), 
        name=user["name"],
        email=user["email"],
        role=user["role"],
        status=user["status"]
        )
    
user_service = UserService()