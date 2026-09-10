# Add to app/api/v1/router.py

from app.api.v1.leave_balance import router as leave_balance_router

# After the other router.include_router(...) calls:
router.include_router(leave_balance_router)
