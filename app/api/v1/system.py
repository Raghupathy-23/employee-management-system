from fastapi import APIRouter


router = APIRouter(
    prefix="/system",
    tags=["System"],
)


@router.get("/info")
def system_info():
    return {
        "application": "Employee Management System",
        "version": "0.1.0",
        "environment": "development",
    }
