import os

__all__ = ["ALGORITHM", "API_DOMAIN_NAME", "OTP_SECRET", "SECRET_KEY", "TOKEN_EXPIRE_MINUTES", "WEB_DOMAIN_NAME"]

TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", 15))
API_DOMAIN_NAME = os.getenv("API_DOMAIN_NAME")
WEB_DOMAIN_NAME = os.getenv("WEB_DOMAIN_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
OTP_SECRET = os.getenv("OTP_SECRET")
ALGORITHM = "HS256"
