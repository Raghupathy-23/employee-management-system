function readCurrentUser() {
  try {
    return JSON.parse(localStorage.getItem("current_user") || "null");
  } catch {
    return null;
  }
}

export default function RoleGate({ allowedRoles = [], children, fallback = null }) {
  const user = readCurrentUser();
  const role = String(user?.role || "").toUpperCase();

  if (!allowedRoles.length || allowedRoles.includes(role)) {
    return children;
  }

  return fallback;
}

export function useCurrentRole() {
  const user = readCurrentUser();
  return String(user?.role || "").toUpperCase();
}
