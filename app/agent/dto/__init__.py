from typing import List
from sqlmodel import Field
from app.core.models import BaseModel
from app.core.database.models import SessionState
from app.core.models import Message


class DocumentDependency(BaseModel):
    session_state: SessionState = Field(description="The session state")
    message_history: List[Message] = Field(default=[], description="The message history")
