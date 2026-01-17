from uuid import UUID
from fastapi import Depends
from app.auth.dependency import get_user_session
from app.auth.dto import AuthUserSession
from app.core.database import Database
from app.core.database.models import Usage
from sqlmodel.ext.asyncio.session import AsyncSession
from app.usage.service import UsageService


async def usage_guard(user_session: AuthUserSession = Depends(get_user_session)) -> Usage:
    """Get or create usage for the user. Subscription checks are handled by better-auth."""
    async def _get_usage(user_id: UUID, db: AsyncSession) -> Usage:
        usage_service = UsageService(db)
        usage = await usage_service.get_usage(user_id)
        if not usage: return await usage_service.create_usage(user_id)
        return usage

    async with Database.async_session() as db:
        usage = await _get_usage(user_session.local_user.id, db)
        return usage
