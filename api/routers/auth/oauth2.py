from fastapi import HTTPException, Request, status
from fastapi.openapi.models import OAuthFlowPassword, OAuthFlows
from fastapi.security import OAuth2


class OAuth2Cookies(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        cookie_name: str,
        scheme_name: str | None = None,
        description: str | None = None,
        scopes: dict[str, str] | None = None,
        auto_error: bool | None = True,
    ):
        if not scopes:
            scopes = {}

        self.cookie_name = cookie_name
        super().__init__(
            flows=OAuthFlows(password=OAuthFlowPassword(tokenUrl=tokenUrl, scopes=scopes)),
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str | None:
        token: str = request.cookies.get(self.cookie_name)
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Impossible de valider le token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return token
