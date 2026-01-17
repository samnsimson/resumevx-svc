import logging
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.model import AuthSession
from app.core.database.models import User
from app.document.dto import DocumentData, UploadDocumentResult
from app.document.service import DocumentService
from app.gateway.dto import EventStatus, ProcessInputDto, EventResponse
from app.session_state.dto import SessionStateDto
from app.session_state.service import SessionStateService
from app.core.constants import GATEWAY_ERROR_PROCESSING_INPUT_DATA


class GatewayService:
    logger = logging.getLogger(__name__)

    def __init__(self, session: AsyncSession):
        self.session = session
        self.document_service = DocumentService(session)
        self.session_state_service = SessionStateService(session)

    async def _get_session_state_dto(self, upload_result: UploadDocumentResult, parsed_content: str, extracted_data: DocumentData, data: ProcessInputDto, local_user: User, auth_session: AuthSession) -> SessionStateDto:
        return SessionStateDto(
            user_id=local_user.id,
            session_token=auth_session.token,
            document_name=upload_result.filename,
            document_url=upload_result.file_url,
            document_parsed=parsed_content,
            document_data=extracted_data,
            generated_document_data=extracted_data,
            template_name=data.template_name,
            job_description=data.job_description,
        )

    async def process_input_data(self, file: UploadFile, data: ProcessInputDto, local_user: User, auth_session: AuthSession):
        try:
            # Upload
            await file.seek(0)
            yield EventResponse(status=EventStatus.uploading)
            upload_result = await self.document_service.upload_document(file, local_user.id)

            # Parse
            await file.seek(0)
            yield EventResponse(status=EventStatus.parsing)
            parsed_content = await self.document_service.parse_document(file=file, mode="accurate")

            # Extract
            yield EventResponse(status=EventStatus.extracting)
            extracted_data = await self.document_service.extract_document(parsed_content)

            # Save
            yield EventResponse(status=EventStatus.saving)
            session_state_dto = await self._get_session_state_dto(upload_result, parsed_content, extracted_data, data, local_user, auth_session)
            await self.session_state_service.create_or_update_session_state(session_state_dto)

            # Success
            yield EventResponse(status=EventStatus.success)
        except Exception as e:
            self.logger.error(GATEWAY_ERROR_PROCESSING_INPUT_DATA.format(error=str(e)))
            yield EventResponse(status=EventStatus.failed, data={"error": str(e)})
