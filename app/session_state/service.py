from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database.models import SessionState
from app.session_state.dto import SessionStateDto
from app.session_state.repository import SessionStateRepository


class SessionStateService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.session_state_repository = SessionStateRepository(session)

    async def get_by_user_id(self, user_id: UUID) -> SessionState | None:
        return await self.session_state_repository.get_by_user_id(user_id)

    async def create_or_update_session_state(self, data: SessionStateDto) -> SessionState:
        session_state = await self.get_by_user_id(data.user_id)
        if not session_state: return await self.create_session_state(SessionStateDto(**data.model_dump(exclude_unset=True)))
        return await self.update_session_state(session_state.id, SessionStateDto(**data.model_dump(exclude_unset=True)))

    async def create_session_state(self, data: SessionStateDto) -> SessionState:
        session_state = SessionState(**data.model_dump(exclude_unset=True))
        return await self.session_state_repository.create(session_state)

    async def update_session_state(self, id: UUID, data: SessionStateDto) -> SessionState:
        session_state = SessionState(**data.model_dump(exclude_unset=True))
        return await self.session_state_repository.update(id, session_state)

    async def delete_session_state(self, user_id: UUID) -> None:
        await self.session_state_repository.delete_by_user_id(user_id)

    async def delete_by_user_id(self, user_id: UUID) -> bool:
        return await self.session_state_repository.delete_by_user_id(user_id)
