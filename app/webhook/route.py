from fastapi import APIRouter
from app.core.database.models import User
from app.core.annotations import TransactionSession
from app.core.utils.decorators.public import public
from app.user.dto import CreateUserDto, UpdateUserDto
from app.user.service import UserService
from app.webhook.dto import UserCreatedPayload, UserDeletedPayload, UserUpdatedPayload

router = APIRouter(tags=["webhook"])


@public
@router.post("/user", operation_id="userCreated", response_model=User)
async def user_created(payload: UserCreatedPayload, session: TransactionSession):
    user_service = UserService(session)
    user_dto = CreateUserDto(auth_user_id=payload.auth_user_id, name=payload.name, username=payload.username, email=payload.email)
    return await user_service.create_local_user(user_dto)


@public
@router.delete("/user", operation_id="userDeleted")
async def user_deleted(payload: UserDeletedPayload, session: TransactionSession):
    user_service = UserService(session)
    return await user_service.delete_local_user(payload.auth_user_id)


@public
@router.put("/user", operation_id="userUpdated")
async def user_updated(payload: UserUpdatedPayload, session: TransactionSession):
    user_service = UserService(session)
    user_dto = UpdateUserDto(**payload.model_dump(exclude_unset=True))
    return await user_service.update_local_user(payload.auth_user_id, user_dto)
