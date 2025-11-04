from sqlalchemy.ext.asyncio import AsyncSession
from repositories.user import UserRepository
from repositories.auth import RefreshTokenRepository
from auth.hashing import hash_password, verify_password
from auth.jwt import create_access_token, create_refresh_token
from schemas.user import UserCreate
from models.user import UserRole


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)
        self.auth_repo = RefreshTokenRepository(session)

    async def register_user(self, user_in: UserCreate):
        existing = await self.user_repo.get_by_email(user_in.email)
        if existing:
            raise ValueError("Email already registered")
        hashed = hash_password(user_in.password)
        role = getattr(user_in, 'role', UserRole.USER.value)
        user = await self.user_repo.create_user(email=user_in.email, password=hashed, role=role)
        return user

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        access = create_access_token(user.id, user.role.value)
        refresh = create_refresh_token(user.id)

        last_refresh = await self.auth_repo.get(user_id=user.id)
        if last_refresh:
            await self.auth_repo.delete(last_refresh)

        await self.auth_repo.add_refresh(user_id=user.id, refresh_token=refresh)
        return {"access": access, "refresh": refresh, "user": user}
