export default function RoleGate({ allowedRoles = [], children, fallback = null }) {
  const user = JSON.parse(localStorage.getItem("current_user") || "null");
  const role = String(user?.role || "").toUpperCase();

  if (!allowedRoles.length || allowedRoles.includes(role)) {
    return children;
  }

  return fallback;
}

export function useCurrentRole() {
  const user = JSON.parse(localStorage.getItem("current_user") || "null");
  return String(user?.role || "").toUpperCase();
}
