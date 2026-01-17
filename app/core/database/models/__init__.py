from typing import Optional, List, Dict, Any
from uuid import uuid4, UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import DateTime, Field, Relationship, func
from datetime import datetime, timezone
from app.document.dto import DocumentData, DocumentMetrics
from app.core.models import BaseModel
from pydantic import field_serializer


def default_time():
    return datetime.now(timezone.utc)


class BaseSQLModel(BaseModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True, nullable=False)
    created_at: datetime = Field(default_factory=default_time, nullable=False, sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=default_time, nullable=False, sa_type=DateTime(timezone=True), sa_column_kwargs={"onupdate": func.now()})


class User(BaseSQLModel, table=True):
    auth_user_id: str = Field(unique=True, index=True, description="User ID from better-auth service")
    name: Optional[str] = Field(default=None, nullable=True, description="Name from better-auth service")
    username: Optional[str] = Field(default=None, nullable=True, unique=True, index=True, description="Username from better-auth service")
    email: Optional[str] = Field(default=None, nullable=True, unique=True, index=True, description="Email for reference (synced from better-auth)")
    resumes: List["Resume"] = Relationship(back_populates="user", cascade_delete=True)
    usage: List["Usage"] = Relationship(back_populates="user", cascade_delete=True)
    session_states: List["SessionState"] = Relationship(back_populates="user", cascade_delete=True)


class Resume(BaseSQLModel, table=True):
    title: str = Field()
    description: Optional[str] = Field(default=None, nullable=True)
    url: Optional[str] = Field(default=None, nullable=True)
    path: Optional[str] = Field(default=None, nullable=True)
    data_original: Optional[str] = Field(default=None, nullable=True)
    data_final: Optional[str] = Field(default=None, nullable=True)
    parsed_final: Optional[str] = Field(default=None, nullable=True)
    parsed_original: Optional[str] = Field(default=None, nullable=True)
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    user: "User" = Relationship(back_populates="resumes")


class Usage(BaseSQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    rewrites: int = Field(default=0)
    downloads: int = Field(default=0)
    uploads: int = Field(default=0)
    user: "User" = Relationship(back_populates="usage")


class SessionState(BaseSQLModel, table=True):
    __tablename__ = "session_state"
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE", index=True, description="User ID - references better-auth user via User model")
    session_token: Optional[str] = Field(default=None, nullable=True, index=True, description="Session token from better-auth for reference")
    template_name: Optional[str] = Field(default=None, nullable=True)
    document_name: Optional[str] = Field(default=None, nullable=True)
    document_url: Optional[str] = Field(default=None, nullable=True)
    document_parsed: Optional[str] = Field(default=None, nullable=True)
    document_data: Optional[Dict[str, Any]] = Field(sa_type=JSONB, default=None, nullable=True)
    document_metrics: Optional[Dict[str, Any]] = Field(sa_type=JSONB, default=None, nullable=True)
    generated_document_name: Optional[str] = Field(default=None, nullable=True)
    genereated_document_url: Optional[str] = Field(default=None, nullable=True)
    generated_document_data: Optional[Dict[str, Any]] = Field(sa_type=JSONB, default=None, nullable=True)
    generated_document_metrics: Optional[Dict[str, Any]] = Field(sa_type=JSONB, default=None, nullable=True)
    job_description: Optional[str] = Field(default=None, nullable=True)
    user: "User" = Relationship(back_populates="session_states")

    @field_serializer("document_data")
    def serialize_document_data(self, document_data: Dict[str, Any] | None) -> DocumentData | None:
        if not document_data: return None
        return DocumentData(**document_data)

    @field_serializer("generated_document_data")
    def serialize_generated_document_data(self, generated_document_data: Dict[str, Any] | None) -> DocumentData | None:
        if not generated_document_data: return None
        return DocumentData(**generated_document_data)

    @field_serializer("document_metrics")
    def serialize_document_metrics(self, document_metrics: Dict[str, Any] | None) -> DocumentMetrics | None:
        if not document_metrics: return None
        return DocumentMetrics(**document_metrics)

    @field_serializer("generated_document_metrics")
    def serialize_generated_document_metrics(self, generated_document_metrics: Dict[str, Any] | None) -> DocumentMetrics | None:
        if not generated_document_metrics: return None
        return DocumentMetrics(**generated_document_metrics)
