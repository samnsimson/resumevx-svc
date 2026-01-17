
from sqlmodel import Field
from app.core.models import BaseModel
from app.auth.model import AuthSession, AuthUser
from app.core.database.models import User


class AuthUserSession(BaseModel):
    user: AuthUser = Field(description="User")
    session: AuthSession = Field(description="Session")
    local_user: User = Field(description="Local user")
