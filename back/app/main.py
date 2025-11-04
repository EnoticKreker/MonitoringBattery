from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.v1.routers import device
from api.v1.routers import battery
from schemas.user import UserCreateAdmin
from services.auth_service import AuthService
from models.base import Base
from core.config import settings
from api.v1.routers import auth, users
from fastapi.middleware.cors import CORSMiddleware
from core.database import AsyncSessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        service = AuthService(session)

        try:
            await service.register_user(
                UserCreateAdmin(
                    email="admin@admin.com",
                    password="1",
                    role="ADMIN"
                )
            )
            await session.commit()
            print("Admin user created")
        except Exception:
            print("Admin user already exists")

    yield

    await engine.dispose()


def create_app(lifespan) -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME,
                  debug=settings.DEBUG, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router)
    app.include_router(battery.router)
    app.include_router(device.router)
    app.include_router(users.router)
    return app


app = create_app(lifespan)
