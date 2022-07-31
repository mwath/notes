from fastapi import HTTPException, status
from passlib.exc import MalformedTokenError, TokenError
from passlib.totp import TOTP, TotpMatch

from .constant import API_DOMAIN_NAME, OTP_SECRET

__all__ = ["TotpFactory", "verify"]

TotpFactory: TOTP = TOTP.using(digits=6, issuer=API_DOMAIN_NAME, secrets={"1": OTP_SECRET})


def verify(totp: TOTP, code: str, last_counter: int = None) -> int:
    try:
        return totp.match(code, last_counter=last_counter).counter
    except MalformedTokenError:
        # It should never happen thanks to pydantic validation
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Code malformé")
    except TokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Code 2FA invalide")
