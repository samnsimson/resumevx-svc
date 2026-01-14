from fastapi import Request, HTTPException
from app.auth.dto import AuthUserSession, UserSession
from app.auth.model import AuthSession, AuthUser
from app.lib.constants import ERROR_UNAUTHORIZED


def get_session_from_request(request: Request) -> AuthSession:
    if not hasattr(request.state, 'session'): raise HTTPException(status_code=401, detail=ERROR_UNAUTHORIZED)
    return AuthSession.model_validate(request.state['session'])


def get_user_from_request(request: Request) -> AuthUser:
    if not hasattr(request.state, 'user'): raise HTTPException(status_code=401, detail=ERROR_UNAUTHORIZED)
    return AuthUser.model_validate(request.state['user'])


def get_user_session(request: Request) -> UserSession:
    user_data = get_user_from_request(request)
    session_data = get_session_from_request(request)
    return AuthUserSession(user=user_data, session=session_data)
