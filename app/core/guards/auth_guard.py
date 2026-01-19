import httpx
from fastapi import HTTPException, Request
from app.auth.dto import AuthUserSession
from app.core.config import settings
from app.core.database import Database
from app.core.database.models import User
from app.user.service import UserService


async def get_auth_session(token: str) -> AuthUserSession | None:
    async with httpx.AsyncClient() as client:
        url = f"{settings.better_auth_url}/get-session"
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


async def get_local_user(auth_user_id: str) -> User | None:
    async with Database.async_session() as db:
        user_service = UserService(db)
        local_user = await user_service.get_local_user(auth_user_id)
        if not local_user: raise HTTPException(status_code=401, detail="Unauthorized")
        return local_user


async def extract_session_data(auth_session: AuthUserSession | None):
    if not auth_session: raise HTTPException(status_code=401, detail="Unauthorized")
    user_data = auth_session["user"] if 'user' in auth_session else None
    session_data = auth_session["session"] if 'session' in auth_session else None
    return user_data, session_data


async def auth_guard(request: Request) -> None:
    endpoint = request.scope.get("endpoint")
    if request.method == "OPTIONS": return
    if endpoint and getattr(endpoint, "is_public", False): return

    token = request.cookies.get(settings.cookie_key, None)
    if not token: raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        auth_session = await get_auth_session(token)
        print(f"auth_session: {auth_session}")
        user_data, session_data = await extract_session_data(auth_session)
        local_user = await get_local_user(user_data['id'])
        setattr(request.state, "user", user_data)
        setattr(request.state, "session", session_data)
        setattr(request.state, "local_user", local_user.model_dump())
    except Exception as e:
        print(f"Error fetching session: {str(e)}")
        raise HTTPException(status_code=401, detail="Unauthorized")
