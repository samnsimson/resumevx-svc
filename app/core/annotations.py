from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.database import Database
from app.auth.dependency import get_user_session
from app.auth.dto import AuthUserSession
from app.core.database.models import Usage
from app.core.guards.usage_guard import usage_guard

DatabaseSession = Annotated[AsyncSession, Depends(Database.get_session)]
TransactionSession = Annotated[AsyncSession, Depends(Database.transaction)]
AuthSession = Annotated[AuthUserSession, Depends(get_user_session)]
UageGuard = Annotated[Usage, Depends(usage_guard)]
