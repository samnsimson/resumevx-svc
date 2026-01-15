from fastapi import APIRouter
from app.database.models import User
from app.lib.annotations import TransactionSession
from app.lib.decorators.public import public
from app.user.dto import CreateUserDto
from app.user.service import UserService
from app.webhook.dto import UserCreatedPayload, UserDeletedPayload

router = APIRouter(tags=["webhook"])


@public
@router.post("/user", operation_id="userCreated", response_model=User)
async def user_created(payload: UserCreatedPayload, session: TransactionSession):
    user_service = UserService(session)
    user_dto = CreateUserDto(id=payload.id, name=payload.name, username=payload.username, email=payload.email)
    return await user_service.create_local_user(user_dto)


@public
@router.delete("/user", operation_id="userDeleted")
async def user_deleted(payload: UserDeletedPayload, session: TransactionSession):
    user_service = UserService(session)
    return await user_service.delete_local_user(payload.id)
