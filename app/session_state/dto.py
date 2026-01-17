from uuid import UUID
from typing import Optional
from sqlmodel import Field
from app.core.models import BaseModel
from app.document.dto import DocumentData, DocumentMetrics


class SessionStateDto(BaseModel):
    user_id: UUID = Field(description="User ID (references better-auth user via User model)")
    session_token: str = Field(description="Session token from better-auth - unique identifier for session state")
    template_name: Optional[str] = Field(default=None, nullable=True, description="Template name")
    document_name: Optional[str] = Field(default=None, nullable=True, description="Document name")
    document_url: Optional[str] = Field(default=None, nullable=True, description="Document URL")
    document_parsed: Optional[str] = Field(default=None, nullable=True, description="Document parsed")
    document_data: Optional[DocumentData] = Field(default=None, nullable=True, description="Document data")
    generated_document_name: Optional[str] = Field(default=None, nullable=True, description="Generated document name")
    genereated_document_url: Optional[str] = Field(default=None, nullable=True, description="Generated document URL")
    generated_document_data: Optional[DocumentData] = Field(default=None, nullable=True, description="Generated document data")
    generated_document_metrics: Optional[DocumentMetrics] = Field(default=None, nullable=True, description="Generated document metrics")
    job_description: Optional[str] = Field(default=None, nullable=True, description="Job description")


class SaveSessionStateDto(BaseModel):
    template_name: Optional[str] = Field(default=None, nullable=True, description="Template name")
    document_name: Optional[str] = Field(default=None, nullable=True, description="Document name")
    document_url: Optional[str] = Field(default=None, nullable=True, description="Document URL")
    document_parsed: Optional[str] = Field(default=None, nullable=True, description="Document parsed")
    document_data: Optional[DocumentData] = Field(default=None, nullable=True, description="Document data")
    generated_document_name: Optional[str] = Field(default=None, nullable=True, description="Generated document name")
    genereated_document_url: Optional[str] = Field(default=None, nullable=True, description="Generated document URL")
    generated_document_data: Optional[DocumentData] = Field(default=None, nullable=True, description="Generated document data")
    generated_document_metrics: Optional[DocumentMetrics] = Field(default=None, nullable=True, description="Generated document metrics")
    job_description: Optional[str] = Field(default=None, nullable=True, description="Job description")
