from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.database import get_db
from app.models.user import User
from app.repositories.audit_repository import AuditRepository
from app.schemas.audit import AuditLogResponse

router = APIRouter(prefix="/audit-logs", tags=["Audit Logs"])
repository = AuditRepository()


@router.get("", response_model=list[AuditLogResponse])
def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    _: User = Depends(require_roles("ADMIN", "HR", "HR_MANAGER")),
    db: Session = Depends(get_db),
):
    return repository.list(db, skip, limit)
