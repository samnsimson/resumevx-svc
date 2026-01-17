import uvicorn
from fastapi import Depends, FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.core.guards.auth_guard import auth_guard
from app.core.limiter import limiter
from app.core.middleware.logging_middleware import LoggingMiddleware
from contextlib import asynccontextmanager
from app.core.database import Database
from app.core.error_handler import setup_error_handlers
from app.auth.route import router as auth_router
from app.user.route import router as user_router
from app.gateway.route import router as gateway_router
from app.webhook.route import router as webhook_router
from app.document.route import router as document_router
from app.session_state.route import router as session_state_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.init_db()
    yield


app = FastAPI(
    title="Frezume SVC",
    description="AI Services for Frezume",
    lifespan=lifespan,
    dependencies=[Depends(auth_guard)]
)

app.state.limiter = limiter


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://frezume.com", "https://www.frezume.com"],
    allow_origin_regex=r"https://.*\.frezume\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
app.add_middleware(LoggingMiddleware)

app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(gateway_router, prefix="/gateway")
app.include_router(document_router, prefix="/document")
app.include_router(session_state_router, prefix="/session-state")
app.include_router(webhook_router, prefix="/webhook")


setup_error_handlers(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
