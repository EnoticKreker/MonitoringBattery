from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from auth.dependencies import admin_required
from repositories.user import UserRepository
from schemas.user import UserRead

router = APIRouter(prefix="/api/v1/users", tags=["users"])

@router.get("", response_model=list[UserRead], dependencies=[Depends(admin_required)])
async def list_users(session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    users = await repo.list()
    return users

@router.put("/{user_id}/role", dependencies=[Depends(admin_required)])
async def set_role(user_id: int, role: str, session: AsyncSession = Depends(get_session)):
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = role
    session.add(user)
    await session.commit()
    return {"status": "ok"}
