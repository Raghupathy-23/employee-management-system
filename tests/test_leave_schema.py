from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.leave import LeaveCreate


def test_leave_end_date_must_not_precede_start_date():
    with pytest.raises(ValidationError):
        LeaveCreate(
            employee_id=1,
            leave_type="ANNUAL",
            start_date=date(2026, 9, 20),
            end_date=date(2026, 9, 19),
            reason="Vacation",
        )
