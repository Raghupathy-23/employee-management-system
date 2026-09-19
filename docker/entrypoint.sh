#!/bin/sh
set -eu

# MySQL's official image can report healthy during its temporary initialization
# phase before the final mysqld process is ready. Wait for a real application
# connection before running Alembic migrations.
python - <<'PY'
import os
import time
import pymysql

url = os.environ["DATABASE_URL"]
prefix = "mysql+pymysql://"
if not url.startswith(prefix):
    raise SystemExit("DATABASE_URL must use the mysql+pymysql:// scheme")

raw = url[len(prefix):]
credentials, database_part = raw.split("/", 1)
auth, host_port = credentials.rsplit("@", 1)
user, password = auth.split(":", 1)
host, port = host_port.rsplit(":", 1)
database = database_part.split("?", 1)[0]

for attempt in range(1, 31):
    try:
        connection = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            connect_timeout=2,
        )
        connection.close()
        print("Database connection is ready.")
        break
    except Exception as exc:
        print(f"Waiting for database ({attempt}/30): {exc}")
        if attempt == 30:
            raise
        time.sleep(2)
PY

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  alembic upgrade head
fi

if [ "${SEED_ROLES:-true}" = "true" ]; then
  # Use -m so Python resolves the repository root (/app) and the app package.
  python -m scripts.seed_roles
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
