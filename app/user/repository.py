from app.database.models import User
from app.database.repository import Repository
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_local_user(self, auth_user_id: str) -> User | None:
        stmt = select(User).where(User.auth_user_id == auth_user_id)
        result = await self.session.exec(stmt)
        return result.first()
