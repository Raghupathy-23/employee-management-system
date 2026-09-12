import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { logout } from "../services/auth";
import NotificationBell from "./NotificationBell";

export default function Layout() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("current_user") || "null");

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">

        {/* Brand */}
        <div className="brand">
          <div className="brand-mark">EM</div>

          <div>
            <strong>Employee</strong>
            <span>Management</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="nav-list">

          <NavLink to="/dashboard" className="nav-link">
            Dashboard
          </NavLink>

          <NavLink to="/departments" className="nav-link">
            Departments
          </NavLink>

          <NavLink to="/employees" className="nav-link">
            Employees
          </NavLink>

          <NavLink to="/attendance" className="nav-link">
            Attendance
          </NavLink>

          <NavLink to="/leaves" className="nav-link">
            Leave
          </NavLink>

          <NavLink to="/notifications" className="nav-link">
            Notifications
          </NavLink>

          {/* Admin only */}
          {user?.role === "ADMIN" && (
            <NavLink to="/roles" className="nav-link">
              Roles
            </NavLink>
          )}

        </nav>

        {/* Logout */}
        <button
          className="logout-button"
          onClick={handleLogout}
        >
          Logout
        </button>

      </aside>

      {/* Main content */}
      <main className="main-content">

        <header className="topbar">

          <div>
            <p className="eyebrow">
              Employee Management System
            </p>

            <h1>Dashboard</h1>
          </div>

          <div className="topbar-actions">

            <NotificationBell />

            <div className="user-chip">

              <span className="avatar">
                {(user?.email || "U")
                  .charAt(0)
                  .toUpperCase()}
              </span>

              <span>
                {user?.email || "User"}
              </span>

            </div>

          </div>

        </header>

        <section className="page-content">
          <Outlet />
        </section>

      </main>
    </div>
  );
}