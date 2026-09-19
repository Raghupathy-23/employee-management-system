from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.api.v1.health import router as health_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware


configure_logging()
settings.validate_runtime()


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title="Employee Management System API",
    description=(
        "Production-style REST API for employee and HR operations, "
        "including authentication, attendance, leave workflows, audit logs and notifications."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

register_exception_handlers(app)
app.add_middleware(RequestLoggingMiddleware)

# Health endpoints stay at the root so container/orchestrator probes do not
# depend on the versioned API namespace.
app.include_router(health_router)
app.include_router(api_router)


@app.get("/", tags=["System"])
def root():
    return {
        "message": "Employee Management System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }
