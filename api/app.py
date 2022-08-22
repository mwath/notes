import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.models.base import db
from api.routers import auth, gateway, page, users
from api.routers.auth.constant import API_DOMAIN_NAME, WEB_DOMAIN_NAME

origins = {API_DOMAIN_NAME, WEB_DOMAIN_NAME}

app = FastAPI(title="NotaBene API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"https://{origin}" for origin in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(gateway.router)
app.include_router(page.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup():
    exception = None
    for retries in range(5):
        try:
            await db.connect()
            break
        except ConnectionRefusedError as e:
            exception = e
            backoff = 2 ** retries / 10
            print(f"Couldn't connect to the database. Retrying in {backoff}s.")
            await asyncio.sleep(backoff)
    else:
        raise exception

    # Check for ENV variables. If one is missing, prevent from starting.
    for key in ("API_DOMAIN_NAME", "OTP_SECRET", "SECRET_KEY", "WEB_DOMAIN_NAME"):
        if getattr(auth, key) is None:
            raise ValueError(f"{key!r} env variable is required but not set.")

    gateway.export_messages()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
