import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { logout } from "../services/auth";

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
        <div className="brand">
          <div className="brand-mark">EM</div>
          <div>
            <strong>Employee</strong>
            <span>Management</span>
          </div>
        </div>

        <nav className="nav-list">
          <NavLink to="/dashboard" className="nav-link">
            Dashboard
          </NavLink>
        </nav>

        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">Employee Management System</p>
            <h1>Dashboard</h1>
          </div>
          <div className="user-chip">
            <span className="avatar">
              {(user?.email || "U").charAt(0).toUpperCase()}
            </span>
            <span>{user?.email || "User"}</span>
          </div>
        </header>

        <section className="page-content">
          <Outlet />
        </section>
      </main>
    </div>
  );
}