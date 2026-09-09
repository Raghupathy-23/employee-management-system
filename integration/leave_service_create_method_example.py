# Do not replace your whole leave_service.py with this file.
# Add the import and balance_service member shown below.

from app.services.leave_balance_service import LeaveBalanceService

# In __init__:
# self.balance_service = LeaveBalanceService()

# In create(), after leave_type validation and before repository.create():
# self.balance_service.validate_request(
#     db,
#     data.employee_id,
#     leave_type,
#     data.start_date,
#     data.end_date,
# )
