from typing import Optional
from sqlmodel import Field
from app.lib.model import BaseModel


class UserCreatedPayload(BaseModel):
    auth_user_id: str = Field(description="User id form better auth")
    name: Optional[str] = Field(default=None, nullable=True, description="Name of the user")
    username: Optional[str] = Field(default=None, nullable=True, description="Username of the user")
    email: Optional[str] = Field(default=None, nullable=True, description="Email of the user")


class UserDeletedPayload(BaseModel):
    auth_user_id: str = Field(description="User id form better auth")


class UserUpdatedPayload(BaseModel):
    auth_user_id: str = Field(description="User id form better auth")
    name: Optional[str] = Field(default=None, nullable=True, description="Name of the user")
    username: Optional[str] = Field(default=None, nullable=True, description="Username of the user")
    email: Optional[str] = Field(default=None, nullable=True, description="Email of the user")
