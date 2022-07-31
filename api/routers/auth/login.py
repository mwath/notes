from fastapi import Depends, HTTPException, status, Response
from passlib.context import CryptContext
from pydantic import BaseModel

from api.models import User, UserPass

from . import jwt
from .oauth2 import OAuth2Cookies
from .constant import TOKEN_EXPIRE_MINUTES


__all__ = [
    "oauth2_scheme",
    "cryptctx",
    "TokenModel",
    "hash_password",
    "is_connected_pass",
    "is_connected",
    "login",
]

oauth2_scheme = OAuth2Cookies(tokenUrl="/auth", cookie_name="access_token")
cryptctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

COOKIE_SETTINGS = {"secure": True, "httponly": True}


class TokenModel(BaseModel):
    # access_token: str
    requires_2fa: bool
    # token_type: str = "bearer"


def login(
    response: Response, user: User, expires: int = TOKEN_EXPIRE_MINUTES, req_2fa: bool = False
) -> TokenModel:
    token = jwt.encode(user.username, expires, requires_2fa=req_2fa)
    response.set_cookie(oauth2_scheme.cookie_name, token, max_age=expires * 60, **COOKIE_SETTINGS)
    return TokenModel(requires_2fa=req_2fa)


def logout(response: Response) -> bool:
    response.delete_cookie(oauth2_scheme.cookie_name, **COOKIE_SETTINGS)
    return True


def hash_password(password: str) -> str:
    return cryptctx.hash(password)


async def is_connected_pass(token: str = Depends(oauth2_scheme)) -> UserPass:
    try:
        req_2fa, username = jwt.decode(token)
        if not req_2fa and (user := await UserPass.get(username)) is not None:
            return user
    except jwt.TokenError:
        pass

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def is_connected(user: UserPass = Depends(is_connected_pass)) -> User:
    return User(**user.dict())
