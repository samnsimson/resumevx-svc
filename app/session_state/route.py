from fastapi import APIRouter
from app.core.annotations import TransactionSession, AuthSession
from app.session_state.service import SessionStateService
from app.core.database.models import SessionState
from app.session_state.dto import SaveSessionStateDto, SessionStateDto

router = APIRouter(tags=["session_state"])


@router.get("", operation_id="getSessionState", response_model=SessionState | None)
async def get_session_state(session: TransactionSession, user_session: AuthSession):
    session_state_service = SessionStateService(session)
    session_state = await session_state_service.get_by_user_id(user_session.local_user.id)
    if not session_state: return None
    return session_state


@router.post("", operation_id="saveSessionState", response_model=SessionState)
async def save_session_state(session: TransactionSession, user_session: AuthSession, data: SaveSessionStateDto):
    session_state_service = SessionStateService(session)
    return await session_state_service.create_or_update_session_state(SessionStateDto(
        user_id=user_session.local_user.id,
        better_auth_session_token=user_session.session.token,
        **data.model_dump()
    ))


@router.delete("", operation_id="clearSessionState", response_model=bool)
async def clear_session_state(session: TransactionSession, user_session: AuthSession):
    session_state_service = SessionStateService(session)
    result = await session_state_service.delete_by_user_id(user_session.local_user.id)
    if not result: return False
    return True
