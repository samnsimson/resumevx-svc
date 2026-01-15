from fastapi import APIRouter
from app.database.models import User
from app.lib.annotations import TransactionSession
from app.lib.decorators.public import public
from app.user.dto import CreateUserDto
from app.user.service import UserService
from app.webhook.dto import UserCreatedPayload

router = APIRouter(tags=["webhook"])


@public
@router.post("/user/create", operation_id="userCreated", response_model=User)
async def user_created(payload: UserCreatedPayload, session: TransactionSession):
    print(f"Creating local user: {payload}")
    user_service = UserService(session)
    user_dto = CreateUserDto(id=payload.id, name=payload.name, username=payload.username, email=payload.email)
    local_user = await user_service.create_local_user(user_dto)
    return local_user
