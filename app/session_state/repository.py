from uuid import UUID
from sqlmodel import select
from app.database.models import SessionState
from app.database.repository import Repository
from sqlmodel.ext.asyncio.session import AsyncSession


class SessionStateRepository(Repository[SessionState]):
    def __init__(self, session: AsyncSession):
        super().__init__(SessionState, session)

    async def get_by_user_id(self, user_id: UUID) -> SessionState | None:
        stmt = select(SessionState).where(SessionState.user_id == user_id)
        result = await self.session.exec(stmt)
        session_state = result.first()
        return session_state

    async def update_by_user_id(self, user_id: UUID, data: SessionState) -> SessionState:
        session_state = await self.get_by_user_id(user_id)
        if not session_state: raise ValueError(f"Session state with user id {user_id} not found")
        session_state.model_construct(**data.model_dump(exclude_unset=True))
        return await self.update(session_state.id, session_state)

    async def delete_by_user_id(self, user_id: UUID) -> bool:
        session_state = await self.get_by_user_id(user_id)
        if not session_state: return False
        await self.delete(session_state.id)
        return True
