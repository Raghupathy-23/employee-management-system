# Attendance, Leave & Role-Based UI

This package is an overlay for the existing React/Vite frontend.

## Added files

- `src/services/attendance.js`
- `src/services/leaves.js`
- `src/services/roles.js`
- `src/components/RoleGate.jsx`
- `src/pages/Attendance.jsx`
- `src/pages/Leaves.jsx`
- `src/pages/Roles.jsx`
- `src/styles/hr.css`

The pages use the existing `src/services/api.js`, so the existing JWT interceptor is reused.

## 1. Add routes

In the existing router/App file, add:

```jsx
import Attendance from "./pages/Attendance";
import Leaves from "./pages/Leaves";
import Roles from "./pages/Roles";
```

Inside the existing `Layout` route:

```jsx
<Route path="/attendance" element={<Attendance />} />
<Route path="/leaves" element={<Leaves />} />
<Route path="/roles" element={<Roles />} />
```

## 2. Add sidebar links

In `Layout.jsx`, add:

```jsx
<NavLink to="/attendance" className="nav-link">
  Attendance
</NavLink>

<NavLink to="/leaves" className="nav-link">
  Leave
</NavLink>

{user?.role === "ADMIN" && (
  <NavLink to="/roles" className="nav-link">
    Roles
  </NavLink>
)}
```

You can keep the Roles page route registered for direct navigation. `Roles.jsx` itself also protects the page and displays an access-restricted message for non-admin users.

## 3. Role-based leave approval

The Leave page shows Approve/Reject actions to:

- ADMIN
- HR
- HR_MANAGER
- MANAGER

This is a frontend visibility rule. The backend must remain the final authority for authorization.

## 4. Expected API endpoints

Attendance:

- `GET /attendance`
- `POST /attendance`
- `GET /attendance/{id}`
- `PATCH /attendance/{id}`
- `DELETE /attendance/{id}`

Leave:

- `GET /leaves`
- `POST /leaves`
- `GET /leaves/{id}`
- `PATCH /leaves/{id}`
- `DELETE /leaves/{id}`
- `PATCH /leaves/{id}/approve`
- `PATCH /leaves/{id}/reject`
- `GET /employees/{employee_id}/leave-balance`

Roles:

- `GET /roles`
- `POST /roles`
- `GET /roles/{id}`
- `PATCH /roles/{id}`
- `DELETE /roles/{id}`

## 5. Important backend-schema note

The UI assumes the existing backend field names:

Attendance:
`employee_id`, `attendance_date`, `check_in`, `check_out`, `status`, `remarks`

Leave:
`employee_id`, `leave_type`, `start_date`, `end_date`, `reason`, `status`, `approval_comment`

Role:
`id`, `name`, `description`

If your existing Role API uses a different update method or field name, change only `src/services/roles.js` or the corresponding form payload.

## 6. CSS

Each page imports `src/styles/hr.css`, so no change to the existing global stylesheet is required.

The design uses:

- clean white panels
- restrained borders
- compact status badges
- responsive tables
- mobile-friendly forms
- consistent buttons and spacing
- clear empty/loading/error states

## 7. No database migration

This frontend package does not change the database and does not require an Alembic migration.
