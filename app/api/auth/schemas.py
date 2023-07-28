from typing import Union
from pydantic import BaseModel
from app.config.settings import api_settings
from app.config.security import get_password_hash


fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "admin",
        "email": "admin@email.com",
        "hashed_password":get_password_hash(api_settings.PASSWORD_ADMIN),
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str