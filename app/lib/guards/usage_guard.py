from uuid import UUID
from fastapi import HTTPException, Request
from app.database import Database
from app.database.models import Usage, Plan, Subscription
from app.auth.model import AuthUser, AuthSession
from app.user.service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from app.subscription.service import SubscriptionService
from app.usage.service import UsageService


async def usage_guard(request: Request) -> Usage:
    user: AuthUser | None = getattr(request.state, "user", None)
    session: AuthSession | None = getattr(request.state, "session", None)
    if not user or not session: raise HTTPException(status_code=401, detail="Unauthorized")

    async def _get_subscription(user_id: UUID, db: AsyncSession) -> Subscription:
        subscription_service = SubscriptionService(db)
        subscription = await subscription_service.get_by_user_id(user_id)
        if not subscription: raise HTTPException(status_code=403, detail="Subscription not found. Please contact support.")
        return subscription

    async def _get_usage(user_id: UUID, db: AsyncSession) -> Usage:
        usage_service = UsageService(db)
        usage = await usage_service.get_usage(user_id)
        if not usage: return await usage_service.create_usage(user_id)
        return usage

    async with Database.async_session() as db:

        user_service = UserService(db)
        local_user = await user_service.get_local_user(user.id)
        if not local_user: raise HTTPException(status_code=404, detail="User not found")
        subscription = await _get_subscription(local_user.id, db)
        usage = await _get_usage(local_user.id, db)
        if subscription.plan == Plan.FREE and usage.rewrites >= 5: raise HTTPException(status_code=403, detail="Usage limit exceeded")
        return usage
