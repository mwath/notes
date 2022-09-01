from asyncpg.exceptions import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, status

from api.models import User, UserCreation, UserPass
from api.routers.auth import Code2FA, hash_password
from api.routers.auth.login import is_connected, is_connected_pass

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


class UserInfo(User):
    has2fa: bool


@router.get("", response_model=list[User])
async def get_all() -> list[User]:
    """Return user's info"""
    return await User.get_all()


@router.get("/me", response_model=UserInfo)
async def me(user: UserPass = Depends(is_connected_pass)) -> UserInfo:
    """Return current user's info"""
    return UserInfo(has2fa=user.totp is not None, **user.dict())


@router.delete("/me", response_model=User)
async def delete_me(twofa: Code2FA, user: UserPass = Depends(is_connected_pass)) -> User:
    """Delete your user."""
    if user.totp is not None:
        if twofa.code is None or not twofa.verify(user):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Un code de double authentification valide est requis pour effectuer cette action",
            )

    return await user.delete()


@router.get("/{id}", response_model=User, dependencies=[Depends(is_connected)])
async def get_user(id: int) -> User:
    """Return a user's info from its id"""
    if user := await User.get(id):
        return user

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Cet utilisateur n'existe pas.")


@router.post("/create", response_model=User)
async def create_account(user: UserCreation) -> User:
    try:
        user.password = hash_password(user.password)
        user = await user.create()
    except UniqueViolationError as e:
        keys = {
            "users_username_key": "Ce nom d'utilisateur",
            "users_email_key": "Cet email",
        }
        raise HTTPException(status.HTTP_409_CONFLICT, f"{keys[e.constraint_name]} existe déjà.")

    return user
