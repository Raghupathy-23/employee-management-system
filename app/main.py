from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as api_router
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware


configure_logging()

app = FastAPI(
    title="Employee Management System API",
    description="REST API for employee and HR management",
    version="0.3.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
register_exception_handlers(app)

# Request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# API routes
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