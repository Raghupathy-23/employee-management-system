import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { listEmployees } from "../services/employees";
import { listDepartments } from "../services/departments";
import { listAttendance } from "../services/attendance";
import { listLeaves } from "../services/leaves";
import { listNotifications } from "../services/notifications";

import "../styles/hr.css";

export default function Dashboard() {
  const user = JSON.parse(
    localStorage.getItem("current_user") || "null"
  );

  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [leaves, setLeaves] = useState([]);
  const [notifications, setNotifications] = useState([]);

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  async function loadDashboard() {
    setLoading(true);

    const results = await Promise.allSettled([
      listEmployees({
        skip: 0,
        limit: 100,
        active_only: false,
      }),

      listDepartments({
        skip: 0,
        limit: 100,
      }),

      listAttendance({
        skip: 0,
        limit: 100,
      }),

      listLeaves({
        skip: 0,
        limit: 100,
      }),

      listNotifications({
        skip: 0,
        limit: 5,
      }),
    ]);

    const [
      employeesResult,
      departmentsResult,
      attendanceResult,
      leavesResult,
      notificationsResult,
    ] = results;

    if (employeesResult.status === "fulfilled") {
  const data = employeesResult.value;

  setEmployees(
    Array.isArray(data)
      ? data
      : data.items || []
  );
}

if (departmentsResult.status === "fulfilled") {
  const data = departmentsResult.value;

  setDepartments(
    Array.isArray(data)
      ? data
      : data.items || []
  );
}

if (attendanceResult.status === "fulfilled") {
  const data = attendanceResult.value;

  setAttendance(
    Array.isArray(data)
      ? data
      : data.items || []
  );
}

if (leavesResult.status === "fulfilled") {
  const data = leavesResult.value;

  setLeaves(
    Array.isArray(data)
      ? data
      : data.items || []
  );
}

if (notificationsResult.status === "fulfilled") {
  const data = notificationsResult.value;

  setNotifications(
    Array.isArray(data)
      ? data
      : data.items || []
  );
}
    setLoading(false);
  }

  const leaveStats = useMemo(() => {
    return {
      pending: leaves.filter(
        (leave) => leave.status === "PENDING"
      ).length,

      approved: leaves.filter(
        (leave) => leave.status === "APPROVED"
      ).length,

      rejected: leaves.filter(
        (leave) => leave.status === "REJECTED"
      ).length,
    };
  }, [leaves]);

  const totalLeaveStats =
    leaveStats.pending +
    leaveStats.approved +
    leaveStats.rejected;

  const attendanceStats = useMemo(() => {
    return {
      present: attendance.filter(
        (item) => item.status === "PRESENT"
      ).length,

      absent: attendance.filter(
        (item) => item.status === "ABSENT"
      ).length,

      halfDay: attendance.filter(
        (item) => item.status === "HALF_DAY"
      ).length,

      onLeave: attendance.filter(
        (item) => item.status === "ON_LEAVE"
      ).length,
    };
  }, [attendance]);

  function getEmployeeName(employeeId) {
    const employee = employees.find(
      (item) => item.id === employeeId
    );

    if (!employee) {
      return `Employee #${employeeId}`;
    }

    return `${employee.first_name} ${employee.last_name}`;
  }

  function getEmployeeCode(employeeId) {
    const employee = employees.find(
      (item) => item.id === employeeId
    );

    return employee?.employee_code || `EMP-${employeeId}`;
  }

  function formatDate(date) {
    if (!date) return "-";

    return new Date(date).toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
    });
  }

  function formatShortDate(date) {
    if (!date) return "-";

    return new Date(date).toLocaleDateString("en-IN", {
      day: "2-digit",
      month: "short",
    });
  }

  function formatStatus(status) {
    if (!status) return "Unknown";

    return status
      .replaceAll("_", " ")
      .toLowerCase()
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  function getUserName() {
    if (!user?.email) {
      return "User";
    }

    return user.email.split("@")[0];
  }

  function getInitials() {
    return getUserName().charAt(0).toUpperCase();
  }

  function getLeaveType(type) {
    if (!type) return "Leave";

    return type
      .replaceAll("_", " ")
      .toLowerCase()
      .replace(/\b\w/g, (char) => char.toUpperCase())
      .replace("Leave", "Leave");
  }

  const recentLeaves = [...leaves]
    .sort(
      (a, b) =>
        new Date(b.created_at || b.start_date) -
        new Date(a.created_at || a.start_date)
    )
    .slice(0, 4);

  const recentNotifications = notifications.slice(0, 4);

  return (
    <div className="dashboard-page">

      {/* =====================================================
          WELCOME
          ===================================================== */}

      <section className="dashboard-welcome">

        <div className="welcome-content">
          <p className="dashboard-greeting">
            Good evening,
          </p>

          <h2>
            {getUserName()} <span>👋</span>
          </h2>

          <p>
            Here's what's happening with your work today.
          </p>
        </div>

        <div className="welcome-quote">
          <span>
            “People are the greatest asset
            <br />
            of any organization.”
          </span>

          <small>— Unknown</small>
        </div>

      </section>

      {/* =====================================================
          STATISTICS
          ===================================================== */}

      <section className="dashboard-stats">

        <div className="dashboard-stat-card stat-blue">

          <div className="stat-icon">
            👥
          </div>

          <div className="stat-content">
            <span>Total Employees</span>

            <strong>
              {loading ? "—" : employees.length}
            </strong>

            <small>
              Employee records
            </small>
          </div>

        </div>


        <div className="dashboard-stat-card stat-green">

          <div className="stat-icon">
            🏢
          </div>

          <div className="stat-content">
            <span>Departments</span>

            <strong>
              {loading ? "—" : departments.length}
            </strong>

            <small>
              Active departments
            </small>
          </div>

        </div>


        <div className="dashboard-stat-card stat-purple">

          <div className="stat-icon">
            ◷
          </div>

          <div className="stat-content">
            <span>Attendance Records</span>

            <strong>
              {loading ? "—" : attendance.length}
            </strong>

            <small>
              Recorded attendance
            </small>
          </div>

        </div>


        <div className="dashboard-stat-card stat-orange">

          <div className="stat-icon">
            📅
          </div>

          <div className="stat-content">
            <span>Leave Requests</span>

            <strong>
              {loading ? "—" : leaves.length}
            </strong>

            <small>
              Total requests
            </small>
          </div>

        </div>

      </section>


      {/* =====================================================
          ANALYTICS
          ===================================================== */}

      <section className="dashboard-analytics">

        {/* Leave Status */}

        <div className="dashboard-chart-card">

          <div className="chart-header">
            <div>
              <h3>Leave Requests by Status</h3>
              <span>Current leave request overview</span>
            </div>
          </div>

          <div className="leave-chart">

            <div className="donut-wrapper">

              <div
                className="leave-donut"
                style={{
                  background: `conic-gradient(
                    #f59e0b 0 ${
                      totalLeaveStats
                        ? (leaveStats.pending /
                            totalLeaveStats) *
                          100
                        : 0
                    }%,

                    #22c55e ${
                      totalLeaveStats
                        ? (leaveStats.pending /
                            totalLeaveStats) *
                          100
                        : 0
                    }% ${
                      totalLeaveStats
                        ? ((leaveStats.pending +
                            leaveStats.approved) /
                            totalLeaveStats) *
                          100
                        : 0
                    }%,

                    #ef4444 ${
                      totalLeaveStats
                        ? ((leaveStats.pending +
                            leaveStats.approved) /
                            totalLeaveStats) *
                          100
                        : 0
                    }% 100%
                  )`,
                }}
              >
                <div className="donut-center">
                  <strong>{totalLeaveStats}</strong>
                  <span>Total</span>
                </div>
              </div>

            </div>


            <div className="chart-legend">

              <div>
                <span className="legend-dot pending" />
                <span>Pending</span>
                <strong>{leaveStats.pending}</strong>
              </div>

              <div>
                <span className="legend-dot approved" />
                <span>Approved</span>
                <strong>{leaveStats.approved}</strong>
              </div>

              <div>
                <span className="legend-dot rejected" />
                <span>Rejected</span>
                <strong>{leaveStats.rejected}</strong>
              </div>

            </div>

          </div>

        </div>


        {/* Attendance Overview */}

        <div className="dashboard-chart-card">

          <div className="chart-header">

            <div>
              <h3>Attendance Overview</h3>
              <span>Current attendance records</span>
            </div>

            <span className="chart-filter">
              Current
            </span>

          </div>

          <div className="attendance-overview">

            <div className="attendance-bar">

              <div
                className="bar-fill present"
                style={{
                  height: `${Math.max(
                    attendanceStats.present * 15,
                    attendanceStats.present
                      ? 12
                      : 0
                  )}%`,
                }}
              />

              <span>Present</span>

            </div>


            <div className="attendance-bar">

              <div
                className="bar-fill absent"
                style={{
                  height: `${Math.max(
                    attendanceStats.absent * 15,
                    attendanceStats.absent
                      ? 12
                      : 0
                  )}%`,
                }}
              />

              <span>Absent</span>

            </div>


            <div className="attendance-bar">

              <div
                className="bar-fill half-day"
                style={{
                  height: `${Math.max(
                    attendanceStats.halfDay * 15,
                    attendanceStats.halfDay
                      ? 12
                      : 0
                  )}%`,
                }}
              />

              <span>Half Day</span>

            </div>


            <div className="attendance-bar">

              <div
                className="bar-fill on-leave"
                style={{
                  height: `${Math.max(
                    attendanceStats.onLeave * 15,
                    attendanceStats.onLeave
                      ? 12
                      : 0
                  )}%`,
                }}
              />

              <span>On Leave</span>

            </div>

          </div>

          <div className="attendance-summary">

            <div>
              <strong>
                {attendanceStats.present}
              </strong>
              <span>Present</span>
            </div>

            <div>
              <strong>
                {attendanceStats.absent}
              </strong>
              <span>Absent</span>
            </div>

            <div>
              <strong>
                {attendanceStats.halfDay}
              </strong>
              <span>Half Day</span>
            </div>

            <div>
              <strong>
                {attendanceStats.onLeave}
              </strong>
              <span>On Leave</span>
            </div>

          </div>

        </div>

      </section>


      {/* =====================================================
          RECENT ACTIVITY
          ===================================================== */}

      <section className="dashboard-activity">

        {/* Recent Leaves */}

        <div className="dashboard-panel">

          <div className="panel-heading">

            <div>
              <h3>Recent Leave Requests</h3>
            </div>

            <Link
              to="/leaves"
              className="view-all"
            >
              View all
            </Link>

          </div>


          <div className="dashboard-table-wrapper">

            <table className="dashboard-table">

              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Leave Type</th>
                  <th>Duration</th>
                  <th>Status</th>
                  <th>Applied On</th>
                </tr>
              </thead>

              <tbody>

                {recentLeaves.length === 0 ? (

                  <tr>
                    <td
                      colSpan="5"
                      className="dashboard-empty"
                    >
                      No leave requests found.
                    </td>
                  </tr>

                ) : (

                  recentLeaves.map((leave) => (

                    <tr key={leave.id}>

                      <td>
                        <div className="employee-cell">

                          <div className="mini-avatar">
                            {getEmployeeCode(
                              leave.employee_id
                            ).slice(-1)}
                          </div>

                          <div>
                            <strong>
                              {getEmployeeCode(
                                leave.employee_id
                              )}
                            </strong>

                            <span>
                              {getEmployeeName(
                                leave.employee_id
                              )}
                            </span>
                          </div>

                        </div>
                      </td>

                      <td>
                        {getLeaveType(
                          leave.leave_type
                        )}
                      </td>

                      <td>
                        {formatShortDate(
                          leave.start_date
                        )}
                        {" - "}
                        {formatShortDate(
                          leave.end_date
                        )}
                      </td>

                      <td>
                        <span
                          className={`dashboard-status status-${String(
                            leave.status || ""
                          ).toLowerCase()}`}
                        >
                          {formatStatus(
                            leave.status
                          )}
                        </span>
                      </td>

                      <td>
                        {formatDate(
                          leave.created_at
                        )}
                      </td>

                    </tr>

                  ))

                )}

              </tbody>

            </table>

          </div>

        </div>


        {/* Notifications */}

        <div className="dashboard-panel">

          <div className="panel-heading">

            <div>
              <h3>Recent Notifications</h3>
            </div>

            <Link
              to="/notifications"
              className="view-all"
            >
              View all
            </Link>

          </div>


          <div className="notification-list">

            {recentNotifications.length === 0 ? (

              <div className="dashboard-empty">
                No notifications found.
              </div>

            ) : (

              recentNotifications.map(
                (notification) => (

                  <div
                    className="dashboard-notification"
                    key={notification.id}
                  >

                    <div className="notification-icon">
                      🔔
                    </div>

                    <div className="notification-content">

                      <strong>
                        {notification.title}
                      </strong>

                      <span>
                        {notification.message}
                      </span>

                    </div>

                    <div className="notification-date">
                      {formatDate(
                        notification.created_at
                      )}
                    </div>

                  </div>

                )
              )

            )}

          </div>

        </div>

      </section>


      {/* =====================================================
          QUICK ACTIONS
          ===================================================== */}

      <section className="dashboard-panel quick-actions-panel">

        <div className="panel-heading">

          <div>
            <h3>Quick Actions</h3>
          </div>

        </div>


        <div className="quick-actions">

          <Link
            to="/employees"
            className="quick-action"
          >
            <div className="quick-action-icon blue">
              👥
            </div>

            <div>
              <strong>View Employees</strong>
              <span>
                Manage employee records
              </span>
            </div>

            <span className="quick-arrow">
              →
            </span>
          </Link>


          <Link
            to="/attendance"
            className="quick-action"
          >
            <div className="quick-action-icon purple">
              ◷
            </div>

            <div>
              <strong>Mark Attendance</strong>
              <span>
                Check attendance records
              </span>
            </div>

            <span className="quick-arrow">
              →
            </span>
          </Link>


          <Link
            to="/leaves"
            className="quick-action"
          >
            <div className="quick-action-icon violet">
              📅
            </div>

            <div>
              <strong>Apply for Leave</strong>
              <span>
                Submit a leave request
              </span>
            </div>

            <span className="quick-arrow">
              →
            </span>
          </Link>


          <Link
            to="/notifications"
            className="quick-action"
          >
            <div className="quick-action-icon indigo">
              🔔
            </div>

            <div>
              <strong>View Notifications</strong>
              <span>
                Check your updates
              </span>
            </div>

            <span className="quick-arrow">
              →
            </span>
          </Link>

        </div>

      </section>

    </div>
  );
}