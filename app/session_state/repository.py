from uuid import UUID
from sqlmodel import select
from app.core.database.models import SessionState
from app.core.database.repository import Repository
from sqlmodel.ext.asyncio.session import AsyncSession


class SessionStateRepository(Repository[SessionState]):
    def __init__(self, session: AsyncSession):
        super().__init__(SessionState, session)

    async def get_by_session_token(self, session_token: str) -> SessionState | None:
        stmt = select(SessionState).where(SessionState.session_token == session_token)
        result = await self.session.exec(stmt)
        session_state = result.first()
        return session_state

    async def get_by_user_id(self, user_id: UUID) -> SessionState | None:
        """Get the first session state for a user. Kept for future use."""
        stmt = select(SessionState).where(SessionState.user_id == user_id)
        result = await self.session.exec(stmt)
        session_state = result.first()
        return session_state

    async def update_by_session_token(self, session_token: str, data: SessionState) -> SessionState:
        session_state = await self.get_by_session_token(session_token)
        if not session_state: raise ValueError(f"Session state with session token {session_token} not found")
        session_state.model_construct(**data.model_dump(exclude_unset=True))
        return await self.update(session_state.id, session_state)

    async def delete_by_session_token(self, session_token: str) -> bool:
        session_state = await self.get_by_session_token(session_token)
        if not session_state: return False
        await self.delete(session_state.id)
        return True

    async def delete_by_user_id(self, user_id: UUID) -> bool:
        """Delete the first session state for a user. Kept for future use."""
        session_state = await self.get_by_user_id(user_id)
        if not session_state: return False
        await self.delete(session_state.id)
        return True
