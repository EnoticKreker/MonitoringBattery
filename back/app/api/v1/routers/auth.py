from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from services.auth_service import AuthService
from schemas.user import UserCreate, UserRead
from schemas.auth import Token
from auth.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    service = AuthService(session)
    try:
        user = await service.register_user(user_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return user


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    service = AuthService(session)
    auth = await service.authenticate_user(form_data.username, form_data.password)
    if not auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    response.set_cookie(
        key="refresh_token",
        value=auth["refresh"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7*24*3600,
        path="/",
    )

    return {
        "access_token": auth["access"],
        "refresh_token": auth["refresh"],
        "token_type": "bearer"
    }


@router.post("/refresh")
async def refresh(
    refresh_token: str | None = Cookie(default=None),
    session: AsyncSession = Depends(get_session)
):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token"
        )

    from auth.jwt import decode_token, create_access_token
    from repositories.auth import RefreshTokenRepository

    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise Exception("Not a refresh token")
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    repo = RefreshTokenRepository(session)
    last_refresh = await repo.get(user_id=user_id)

    if not last_refresh or last_refresh.token != refresh_token or last_refresh.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not valid"
        )

    access = create_access_token(user_id, role="USER")

    return {"access_token": access, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def me(user=Depends(get_current_user)):
    return user
