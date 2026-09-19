import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for predictable application errors."""

    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unexpected_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "detail": "An unexpected error occurred.",
                "path": request.url.path,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "detail": exc.errors(),
                "path": request.url.path,
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_exception_handler(request: Request, exc: IntegrityError):
        logger.warning("Database integrity error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=409,
            content={
                "error": "database_conflict",
                "detail": "The request conflicts with existing data.",
                "path": request.url.path,
            },
        )
