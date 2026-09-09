# Employee Management Frontend — Phases 1–3

This package contains the first three frontend development phases for the existing FastAPI Employee Management API.

## Phase 1 — React/Vite setup

- React + Vite
- JavaScript/JSX
- CSS
- Axios
- React Router
- Environment-based API URL

## Phase 2 — Responsive application layout

- Sidebar navigation
- Top bar
- Responsive desktop/tablet/mobile layout
- Reusable protected-route and layout components

## Phase 3 — Authentication + dashboard

- Login using the existing `/api/v1/auth/login` endpoint
- JWT token stored in localStorage
- Bearer token automatically added to API requests
- `/api/v1/auth/me` used to load the current user
- Protected dashboard route
- Dashboard calls:
  - `/api/v1/system/info`
  - `/api/v1/system/database`

## Prerequisites

- Node.js and npm
- Existing FastAPI backend running on `http://127.0.0.1:8000`
- Backend authentication endpoint working

## Run

Open a terminal in this frontend folder:

```powershell
npm install
```

Create `.env` from `.env.example` if you want to configure the API URL:

```powershell
copy .env.example .env
```

Start the frontend:

```powershell
npm run dev
```

Vite will show the local URL, normally:

```text
http://localhost:5173
```

## Build check

```powershell
npm run build
```

## Testing the three phases

### 1. Login

Open the frontend and go to `/login`.

Use a valid user already created in your backend database.

Expected:

- successful login redirects to `/dashboard`
- token is stored in the browser
- current user email appears in the top bar

### 2. Protected route

Open `/dashboard` without a token.

Expected:

- application redirects to `/login`

### 3. Backend connection

After login, the dashboard should show:

- Backend: Connected
- Database: Connected

If these fail, check that the FastAPI backend is running and that the API URL in `.env` is correct.

## Important backend note

The frontend expects the existing login endpoint to accept OAuth2-style form data:

```text
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded
username=<email>
password=<password>
```

It also expects the response to contain:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

If your current backend uses a different login request/response shape, only `src/services/auth.js` needs to be adjusted.

## Next frontend phases

After these three phases are verified, continue in this order:

1. Departments UI
2. Employees UI
3. Attendance UI
4. Leave UI
5. Leave approval/rejection UI
6. Audit information
7. Loading/error/empty states
8. Frontend automated tests
9. Full integration testing
