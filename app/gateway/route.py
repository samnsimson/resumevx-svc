from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from app.gateway.dto import ProcessInputDto
from app.gateway.service import GatewayService
from app.core.annotations import AuthSession, TransactionSession

router = APIRouter(tags=['Gateway'])


@router.post('/process-input-data', operation_id='processInputData')
async def process_input_data(
        session: TransactionSession,
        user_session: AuthSession,
        template_name: str = Form(...),
        job_description: str = Form(...),
        file: UploadFile = File(...)):
    gateway_service = GatewayService(session)
    data = ProcessInputDto(template_name=template_name, job_description=job_description)
    headers = {"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"}

    async def stream():
        async for event in gateway_service.process_input_data(file, data, user_session.local_user, user_session.session):
            yield f"data: {event.model_dump_json()}\n\n"

    return StreamingResponse(stream(), media_type='text/event-stream', headers=headers)
