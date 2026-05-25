import os
from dotenv import load_dotenv
from itsdangerous import  URLSafeTimedSerializer, BadSignature
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi import HTTPException
load_dotenv()

AUTH_ENABLED = os.getenv("AUTH_ENABLED", "false").lower() == "true"
AUTH_USERNAME = os.getenv("AUTH_USERNAME",  "admin")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD",  "changeme")
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

serializer = URLSafeTimedSerializer(SECRET_KEY)


def create_session_cookies(username: str)-> str:
    """ data plus the hash to stamp out usernme"""
    return serializer.dumps(username) 
   
def verify_session_cookies(cookie: str)-> bool:
    """ return true if the session (?) is still valid"""
    try:
        serializer.loads(cookie, max_age=86400)
        return True
    except BadSignature:
        return False

def is_authenticated(request: Request)-> bool:
    """ check if the incoming requests has a valid session. """
    if not AUTH_ENABLED:
        return True
    cookies = request.cookies.get("session")
    if not cookies:
        return False
    return verify_session_cookies(cookies)

def login(username: str, password: str)-> bool:
    """ check if credentials match the value in the .env"""
    return username == AUTH_USERNAME and password == AUTH_PASSWORD

def require_auth(request: Request):
    if not AUTH_ENABLED:
        return
    if not is_authenticated(request):
        raise HTTPException(status_code=401, detail="Not authenticated")