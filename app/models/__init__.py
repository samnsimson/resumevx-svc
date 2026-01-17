from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field


class Message(BaseModel):
    id: str = Field(description="The message id")
    role: Literal["user", "assistant"] = Field(description="The message role")
    content: str = Field(description="The message content")
    timestamp: datetime = Field(description="The message timestamp")
