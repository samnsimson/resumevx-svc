from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.models import User
from app.user.dto import CreateUserDto
from app.user.repository import UserRepository
from fastapi import HTTPException


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)

    async def get_user(self, id: UUID) -> User:
        user = await self.user_repository.get(id)
        if not user: raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_local_user(self, auth_user_id: str) -> User | None:
        return await self.user_repository.get_local_user(auth_user_id)

    async def create_local_user(self, data: CreateUserDto) -> User:
        return await self.user_repository.create_local_user(data)

    async def update_user(self, user_id: UUID, data: User, commit: bool = False) -> User:
        return await self.user_repository.update(user_id, data, commit=commit)

    async def delete_user(self, user_id: UUID) -> None:
        await self.user_repository.delete(user_id)
