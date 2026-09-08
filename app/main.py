from fastapi import FastAPI

from app.api.v1.router import router as api_router


app = FastAPI(
    title="Employee Management System API",
    description="REST API for employee and HR management",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Employee Management System API",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(api_router)
