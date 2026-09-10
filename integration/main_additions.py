# Add to app/main.py. Merge these lines with your existing imports/app setup.

from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware

configure_logging()

# After app = FastAPI(...):
register_exception_handlers(app)
app.add_middleware(RequestLoggingMiddleware)
