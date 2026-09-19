# Frontend Notes

The React client is a Vite application. It communicates with the FastAPI backend through Axios and reads the API base URL from `VITE_API_BASE_URL`.

## Local development

```powershell
npm ci
npm run dev -- --host 0.0.0.0
```

## Production build

```powershell
npm ci
npm run build
```

The production Docker image uses Nginx and supports React Router SPA fallback through `try_files`.

## Authentication

The client stores the access token and current-user information in browser local storage for this portfolio project. The Axios interceptor attaches the bearer token to API requests and redirects to `/login` after a 401 response.

For a higher-security production application, a future iteration should move session handling to secure, HttpOnly cookies with CSRF protection.
