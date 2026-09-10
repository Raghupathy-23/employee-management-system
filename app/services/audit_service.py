import json

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


class AuditService:
    def record(
        self,
        db: Session,
        action: str,
        user_id: int | None = None,
        resource: str | None = None,
        resource_id: int | str | None = None,
        details: dict | None = None,
    ) -> AuditLog:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=str(resource_id) if resource_id is not None else None,
            details=json.dumps(details, default=str) if details else None,
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry
