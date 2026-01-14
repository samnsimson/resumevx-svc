import httpx
from fastapi import HTTPException, Request
from app.config import settings


async def get_auth_session(token: str):
    async with httpx.AsyncClient() as client:
        url = f"{settings.better_auth_url}/get-session"
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


async def auth_guard(request: Request) -> None:
    endpoint = request.scope.get("endpoint")
    if request.method == "OPTIONS": return
    if endpoint and getattr(endpoint, "is_public", False): return

    token = request.cookies.get('better-auth.session_token', None)
    if not token: raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        token = token.split('.')[0] if '.' in token else token
        response_data = await get_auth_session(token)
        user_data = response_data["user"] if 'user' in response_data else None
        session_data = response_data["session"] if 'session' in response_data else None
        setattr(request.state, "user", user_data)
        setattr(request.state, "session", session_data)
    except Exception as e:
        print(f"Error fetching session: {str(e)}")
        raise HTTPException(status_code=401, detail="Unauthorized")
