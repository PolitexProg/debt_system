from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.core.database import create_table
from app.core.security import fastapi_users, auth_backend
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.api import debts, settings, monitoring

app = FastAPI(
    title="Debt Tracker API",
    description="Debt tracking system with FastAPI-Users authentication",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

app.include_router(debts.router)
app.include_router(settings.router)
app.include_router(monitoring.router)

@app.on_event("startup")
async def on_startup():
    await create_table()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)