import hashlib
from sqlmodel.ext.asyncio.session import AsyncSession


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        return self._hash_password(password) == hashed_password
