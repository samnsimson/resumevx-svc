import httpx
from fastapi import HTTPException, Request
from app.auth.dto import AuthUserSession
from app.config import settings


async def get_auth_session(token: str) -> AuthUserSession | None:
    print(f"Token: {token}")
    async with httpx.AsyncClient() as client:
        url = f"{settings.better_auth_url}/get-session"
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


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
        # token = token.split('.')[0] if '.' in token else token
        auth_session = await get_auth_session(token)
        user_data, session_data = await extract_session_data(auth_session)
        setattr(request.state, "user", user_data)
        setattr(request.state, "session", session_data)
    except Exception as e:
        print(f"Error fetching session: {str(e)}")
        raise HTTPException(status_code=401, detail="Unauthorized")
