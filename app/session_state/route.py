from fastapi import APIRouter, HTTPException
from app.lib.annotations import TransactionSession, AuthSession
from app.session_state.service import SessionStateService
from app.user.service import UserService
from app.database.models import SessionState
from app.session_state.dto import SaveSessionStateDto, SessionStateDto

router = APIRouter(tags=["session_state"])


@router.get("", operation_id="getSessionState", response_model=SessionState | None)
async def get_session_state(session: TransactionSession, user_session: AuthSession):
    session_state_service = SessionStateService(session)
    user_service = UserService(session)

    user = await user_service.get_local_user(user_session.user.id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    session_state = await session_state_service.get_by_user_id(user.id)
    if not session_state: return None
    return session_state


@router.post("", operation_id="saveSessionState", response_model=SessionState)
async def save_session_state(session: TransactionSession, user_session: AuthSession, data: SaveSessionStateDto):
    session_state_service = SessionStateService(session)
    user_service = UserService(session)

    user = await user_service.get_local_user(user_session.user.id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    session_state_dto = SessionStateDto(
        user_id=user.id,
        better_auth_session_token=user_session.session.token,
        **data.model_dump()
    )
    session_state = await session_state_service.create_or_update_session_state(session_state_dto)
    return session_state


@router.delete("", operation_id="clearSessionState", response_model=bool)
async def clear_session_state(session: TransactionSession, user_session: AuthSession):
    session_state_service = SessionStateService(session)
    user_service = UserService(session)

    user = await user_service.get_local_user(user_session.user.id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    result = await session_state_service.delete_by_user_id(user.id)
    if not result: return False
    return True
