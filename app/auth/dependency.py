from fastapi import Request, HTTPException
from app.auth.dto import AuthUserSession
from app.auth.model import AuthSession, AuthUser
from app.database.models import User
from app.lib.constants import ERROR_UNAUTHORIZED


def get_session_from_request(request: Request) -> AuthSession:
    if not hasattr(request.state, 'session'): raise HTTPException(status_code=401, detail=ERROR_UNAUTHORIZED)
    session = getattr(request.state, 'session', None)
    return AuthSession(**session)


def get_user_from_request(request: Request) -> AuthUser:
    if not hasattr(request.state, 'user'): raise HTTPException(status_code=401, detail=ERROR_UNAUTHORIZED)
    user = getattr(request.state, 'user', None)
    return AuthUser(**user)


def get_local_user_from_request(request: Request) -> User:
    if not hasattr(request.state, 'local_user'): raise HTTPException(status_code=401, detail=ERROR_UNAUTHORIZED)
    local_user = getattr(request.state, 'local_user', None)
    return User(**local_user)


def get_user_session(request: Request) -> AuthUserSession:
    user_data = get_user_from_request(request)
    session_data = get_session_from_request(request)
    local_user = get_local_user_from_request(request)
    return AuthUserSession(user=user_data, session=session_data, local_user=local_user)
