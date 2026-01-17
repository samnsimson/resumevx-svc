from typing import Optional
from sqlmodel import Field
from app.core.models import BaseModel


class CreateUserDto(BaseModel):
    auth_user_id: str = Field(description='Auth user id')
    name: Optional[str] = Field(default=None, nullable=True, description="Name")
    username: Optional[str] = Field(default=None, nullable=True, description="Username")
    email: Optional[str] = Field(default=None, nullable=True, description="Email address")


class UpdateUserDto(BaseModel):
    name: Optional[str] = Field(default=None, nullable=True, description="Name")
    username: Optional[str] = Field(default=None, nullable=True, description="Username")
    email: Optional[str] = Field(default=None, nullable=True, description="Email address")
