from uuid import UUID
from fastapi import APIRouter, HTTPException
from app.core.database.models import User
from app.core.annotations import AuthSession, DatabaseSession
from app.user.service import UserService

router = APIRouter(tags=["user"])


@router.get("/me", operation_id="getCurrentUser", response_model=User)
async def get_current_user(user_session: AuthSession, session: DatabaseSession):
    return user_session.local_user


@router.get("/{id}", operation_id="getUser", response_model=User)
async def get_user(id: UUID, session: DatabaseSession, user_session: AuthSession):
    local_user = user_session.local_user
    if local_user.id != id: raise HTTPException(status_code=403, detail="Forbidden: You can only access your own data")
    user_service = UserService(session)
    return await user_service.get_user(id)
