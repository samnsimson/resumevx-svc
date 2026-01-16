
from sqlmodel import Field
from app.lib.model import BaseModel
from app.auth.model import AuthSession, AuthUser
from app.database.models import User


class AuthUserSession(BaseModel):
    user: AuthUser = Field(description="User")
    session: AuthSession = Field(description="Session")
    local_user: User = Field(description="Local user")
