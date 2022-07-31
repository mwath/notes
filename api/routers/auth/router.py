import json
from typing import Optional

from api.models import User, UserPass
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, constr

from . import jwt, totp
from .login import (
    COOKIE_SETTINGS,
    TokenModel,
    cryptctx,
    is_connected,
    is_connected_pass,
    logout,
    oauth2_scheme,
    login,
)

__all__ = ["router"]

router = APIRouter(
    prefix="/auth",
    tags=["security"],
)


class Create2FA(BaseModel):
    uri: str


class Code2FA(BaseModel):
    code: Optional[constr(regex=r"^\d{6}$")]  # noqa: F722

    async def verify(self, user: UserPass, uri: str = None) -> totp.TOTP:
        otp = totp.TotpFactory.from_source(uri or user.totp)
        await user.updateTOTPCounter(totp.verify(otp, self.code, user.totp_counter))
        return otp


class SuccessModel(BaseModel):
    success: bool


@router.post("", response_model=TokenModel)
async def authenticate(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UserPass.get(form_data.username)
    if user is None or not cryptctx.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.totp is not None:
        result = login(response, user, expires=20, req_2fa=True)

        # This is a hack to allow 2FA authentication in swagger ui
        # Set `Client credentials location` to `request body` then put your TOTP code in the `client_id` field
        # This should be only allowed in the dev environnement
        if form_data.client_id is not None:
            return await verify_2fa(Code2FA(code=form_data.client_id), result.access_token)

        return result

    return login(response, user)


@router.post("/logout", response_model=SuccessModel)
async def authenticate(response: Response):
    return SuccessModel(success=logout(response))


@router.get("/2fa/new", response_model=Create2FA)
async def new_2fa(response: Response, user: User = Depends(is_connected)):
    otp = totp.TotpFactory.new()
    uri = otp.to_uri(label=user.username)

    # The token expires in 20 minutes
    expires = 20
    token = jwt.encode({"uri": uri, "uid": user.id}, expires)
    response.set_cookie("twofachal", token, max_age=expires * 60, **COOKIE_SETTINGS)

    return Create2FA(uri=uri)


@router.post("/2fa/enable")
async def enable_2fa(
    response: Response,
    twofa: Code2FA,
    twofachal: str = Cookie(),
    user: UserPass = Depends(is_connected_pass),
):
    response.delete_cookie("twofachal", **COOKIE_SETTINGS)

    try:
        data = json.loads(jwt.decode(twofachal)[1])
    except jwt.TokenError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))

    if data.get("uid") != user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token invalide")

    if user.totp is not None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "L'authentification à double facteur est déjà activée sur ce compte.",
        )

    # Enable 2FA on this account
    if otp := await twofa.verify(user, uri=data.get("uri")):
        await user.enable_2fa(otp.to_json())


@router.post("/2fa/disable")
async def disable_2fa(twofa: Code2FA, user: UserPass = Depends(is_connected_pass)):
    if user.totp is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "L'authentification à double facteur n'est pas activée sur ce compte.",
        )

    if await twofa.verify(user):
        # Disable 2FA on this account
        await user.disable_2fa()


@router.post("/2fa/verify", response_model=TokenModel)
async def verify_2fa(response: Response, twofa: Code2FA, token: str = Depends(oauth2_scheme)):
    try:
        req_2fa, username = jwt.decode(token)
        if not req_2fa or (user := await UserPass.get(username)) is None:
            raise jwt.TokenError("Wrong State")
    except jwt.TokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if await twofa.verify(user):
        return login(response, user)
