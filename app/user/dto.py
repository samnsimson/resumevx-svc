from typing import Optional
from sqlmodel import Field
from app.lib.model import BaseModel


class CreateUserDto(BaseModel):
    id: str = Field(description='Auth user id')
    name: Optional[str] = Field(default=None, nullable=True, description="Name")
    username: Optional[str] = Field(default=None, nullable=True, description="Username")
    email: Optional[str] = Field(default=None, nullable=True, description="Email address")
