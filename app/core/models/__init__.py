from typing import Literal
from datetime import datetime
from pydantic import Field, ConfigDict
from sqlmodel import SQLModel
from pydantic.alias_generators import to_camel


class BaseModel(SQLModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class Message(BaseModel):
    id: str = Field(description="The message id")
    role: Literal["user", "assistant"] = Field(description="The message role")
    content: str = Field(description="The message content")
    timestamp: datetime = Field(description="The message timestamp")
