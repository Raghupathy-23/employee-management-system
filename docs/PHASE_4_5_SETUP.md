# Frontend Phase 4 + Phase 5

## Added
- `src/pages/Departments.jsx`
- `src/pages/Employees.jsx`
- `src/services/departments.js`
- `src/services/employees.js`

## Router
In your existing React router, add:

```jsx
import Departments from "./pages/Departments";
import Employees from "./pages/Employees";

<Route path="/departments" element={<Departments />} />
<Route path="/employees" element={<Employees />} />
```

Keep the existing protected-route wrapper if your app uses one.

## Navigation
Add links to the existing layout/navigation:

```jsx
<Link to="/departments">Departments</Link>
<Link to="/employees">Employees</Link>
```

## CSS
The pages use these classes:
`page`, `page-header`, `content-card`, `data-form`, `employee-form`,
`filter-row`, `table-wrapper`, `data-table`, `table-actions`,
`form-actions`, `form-wide`, `checkbox-label`, `secondary-button`.

If they do not already exist, add suitable styles to `src/index.css`.
A responsive table should use `overflow-x: auto` on `.table-wrapper`.

## Run
From the existing project root:

```powershell
npm install
npm run dev
```

Keep FastAPI running separately:

```powershell
uvicorn app.main:app --reload
```

Then log in and open:

```text
http://localhost:5173/departments
http://localhost:5173/employees
```

No Alembic migration is required for these frontend-only changes.

## Important
Employee creation requires a valid existing `user_id` because the current backend `EmployeeCreate` schema requires it. The UI therefore asks for User ID rather than inventing a user lookup.
