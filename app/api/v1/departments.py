from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from app.services.department_service import DepartmentService

router = APIRouter(prefix="/departments", tags=["Departments"])
service = DepartmentService()

@router.post("", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(payload: DepartmentCreate, db: Session = Depends(get_db)):
    try:
        return service.create(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@router.get("", response_model=list[DepartmentResponse])
def list_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if limit > 100:
        raise HTTPException(status_code=400, detail="limit cannot exceed 100")
    return service.list(db, skip, limit)

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = service.get(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.patch("/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int, payload: DepartmentUpdate, db: Session = Depends(get_db)):
    try:
        department = service.update(db, department_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    if not service.delete(db, department_id):
        raise HTTPException(status_code=404, detail="Department not found")
