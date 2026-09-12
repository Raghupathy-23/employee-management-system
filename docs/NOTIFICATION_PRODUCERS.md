# Notification producers

The notification table/API is the foundation. Business services should create notifications when an important state change occurs.

## Leave approval example

In the existing `LeaveApprovalService`, after the leave status is changed, resolve the employee's `user_id` and create a notification:

```python
from app.models.employee import Employee
from app.schemas.notification import NotificationCreate
from app.services.notification_service import NotificationService

employee = db.get(Employee, leave.employee_id)
if employee and employee.user_id:
    NotificationService().create(
        db,
        NotificationCreate(
            user_id=employee.user_id,
            notification_type="LEAVE",
            title="Leave request approved",
            message=f"Your leave request from {leave.start_date} to {leave.end_date} was approved.",
            link=f"/leaves/{leave.id}",
        ),
    )
```

For rejection, use a different title/message. Keep notification creation inside the same business workflow so the event cannot be forgotten.

## Future producers

The same service can be reused for:

- attendance exceptions
- leave submission/approval/rejection
- employee status changes
- role or department changes
- workflow/escalation reminders

Email, push, or scheduled escalation should be added later as separate delivery capabilities.
