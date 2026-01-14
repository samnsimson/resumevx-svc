
from sqlmodel import Field
from app.lib.model import BaseModel
from app.auth.model import AuthSession, AuthUser


class AuthUserSession(BaseModel):
    user: AuthUser = Field(description="User")
    session: AuthSession = Field(description="Session")
