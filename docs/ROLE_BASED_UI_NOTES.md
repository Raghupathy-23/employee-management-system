# Role-Based UI Notes

The current user is read from:

```js
localStorage.getItem("current_user")
```

The expected backend `/auth/me` response contains:

```json
{
  "id": 1,
  "email": "admin@example.com",
  "role": "ADMIN",
  "is_active": true
}
```

`RoleGate` provides a reusable client-side gate:

```jsx
<RoleGate allowedRoles={["ADMIN"]}>
  <AdminOnlyContent />
</RoleGate>
```

Client-side role checks are for presentation and navigation only. They do not replace backend authorization.

For the current implementation:

- Roles administration: ADMIN only
- Leave approval controls: ADMIN, HR, HR_MANAGER, MANAGER
- Attendance and Leave pages remain available through the normal authenticated layout

If the backend defines a different authorization matrix, update the allowed role arrays in the UI to match it.
