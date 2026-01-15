from app.database.models import User
from app.database.repository import Repository
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.user.dto import CreateUserDto, UpdateUserDto


class UserRepository(Repository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def create_local_user(self, data: CreateUserDto) -> User:
        user = User(auth_user_id=data.auth_user_id, username=data.username, email=data.email, name=data.name)
        return await self.create(user)

    async def get_local_user(self, auth_user_id: str) -> User | None:
        stmt = select(User).where(User.auth_user_id == auth_user_id)
        result = await self.session.exec(stmt)
        return result.first()

    async def delete_local_user(self, auth_user_id: str) -> bool:
        user = await self.get_local_user(auth_user_id)
        if not user: return False
        await self.delete(user.id)
        return True

    async def update_local_user(self, auth_user_id: str, data: UpdateUserDto) -> User:
        user = await self.get_local_user(auth_user_id)
        if not user: raise ValueError(f"User with auth user id {auth_user_id} not found")
        user_data = user.model_construct(**data.model_dump(exclude_unset=True))
        return await self.update(user.id, user_data)
