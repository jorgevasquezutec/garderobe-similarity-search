import jwt
from jwt import PyJWTError
from fastapi import HTTPException, Security,status
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_403_FORBIDDEN
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
from app.config.jwt import ALGORITHM
from app.api.auth.schemas import TokenData,fake_users_db,UserInDB,User
from app.api.auth.repository import get_user
from fastapi import Depends
from typing import Annotated



reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login/access-token")

async def get_current_user(token: str = Security(reusable_oauth2)):
    try:
        payload = jwt.decode(token, settings.api_settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData(**payload)
    except PyJWTError as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

