# Frontend integration — cleanup + notifications

This overlay keeps the existing React/Vite structure and adds the notification center while fixing the employee lookup limit that previously caused `422 less_than_equal` errors.

## 1. Copy the overlay

Copy the `src/` files into the existing frontend source tree.

The Attendance and Leave pages already use `limit: 100` for employee lookups. Do not change this back to 200 because the backend currently validates `limit <= 100`.

## 2. Add Notifications route

In `src/App.jsx`:

```jsx
import Notifications from "./pages/Notifications";
```

Inside the protected/layout route group:

```jsx
<Route path="/notifications" element={<Notifications />} />
```

## 3. Add the notification bell

Import:

```jsx
import NotificationBell from "./NotificationBell";
```

Place `<NotificationBell />` in the existing authenticated header/top bar in `Layout.jsx`.

Keep the existing sidebar and role logic unchanged.

## 4. Optional sidebar link

Add this alongside Dashboard, Departments, Employees, Attendance and Leave:

```jsx
<NavLink to="/notifications" className="nav-link">Notifications</NavLink>
```

## 5. API base URL

No change is required if the existing `src/services/api.js` already uses:

```js
import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/v1"
```

## 6. Cleanup already included

- Employee lookup limit fixed from 200 to 100.
- Notification API isolated in `services/notifications.js`.
- Notification UI is split into a reusable bell and full-page view.
- API errors are surfaced without replacing the existing Axios interceptor behavior.
- Polling is limited to 30 seconds and cleaned up on unmount.
