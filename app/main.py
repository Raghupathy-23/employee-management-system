from fastapi import FastAPI

from app.api.v1.router import router as api_router

from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Employee Management System API",
    description="REST API for employee and HR management",
    version="0.3.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_exception_handlers(app)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "Employee Management System API",
        "version": "0.3.0",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/health/readiness")
def readiness_check():
    return {"status": "ready"}