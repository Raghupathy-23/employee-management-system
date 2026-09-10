import { useEffect, useState } from "react";
import {
  createAttendance,
  deleteAttendance,
  listAttendance,
  updateAttendance,
} from "../services/attendance";
import { listEmployees } from "../services/employees";
import "../styles/hr.css";

const STATUSES = ["PRESENT", "ABSENT", "HALF_DAY", "ON_LEAVE"];

const emptyForm = {
  employee_id: "",
  attendance_date: "",
  check_in: "",
  check_out: "",
  status: "PRESENT",
  remarks: "",
};

function formatTime(value) {
  if (!value) return "—";
  return String(value).slice(0, 5);
}

export default function Attendance() {
  const [rows, setRows] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [filters, setFilters] = useState({ employee_id: "", status: "", date: "" });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const params = {};
      if (filters.employee_id) params.employee_id = filters.employee_id;
      if (filters.status) params.status = filters.status;
      if (filters.date) params.attendance_date = filters.date;
      const [attendanceData, employeeData] = await Promise.all([
        listAttendance(params),
        listEmployees({ limit: 100 }),
      ]);
      setRows(Array.isArray(attendanceData) ? attendanceData : attendanceData.items || []);
      setEmployees(Array.isArray(employeeData) ? employeeData : employeeData.items || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load attendance records.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  function change(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function startEdit(row) {
    setEditingId(row.id);
    setForm({
      employee_id: row.employee_id ?? "",
      attendance_date: row.attendance_date ?? "",
      check_in: formatTime(row.check_in) === "—" ? "" : formatTime(row.check_in),
      check_out: formatTime(row.check_out) === "—" ? "" : formatTime(row.check_out),
      status: row.status || "PRESENT",
      remarks: row.remarks || "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function resetForm() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const payload = {
        ...form,
        employee_id: Number(form.employee_id),
        check_in: form.check_in || null,
        check_out: form.check_out || null,
      };
      if (editingId) {
        await updateAttendance(editingId, payload);
      } else {
        await createAttendance(payload);
      }
      resetForm();
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to save attendance.");
    } finally {
      setSaving(false);
    }
  }

  async function remove(id) {
    if (!window.confirm("Delete this attendance record?")) return;
    try {
      await deleteAttendance(id);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete the record.");
    }
  }

  function employeeName(id) {
    const employee = employees.find((item) => item.id === id);
    if (!employee) return `Employee #${id}`;
    return `${employee.first_name || ""} ${employee.last_name || ""}`.trim() || employee.employee_code || `Employee #${id}`;
  }

  return (
    <div className="hr-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">HR Operations</p>
          <h2>Attendance</h2>
          <p className="page-subtitle">Record and manage daily employee attendance.</p>
        </div>
        <div className="stat-pill">{rows.length} records</div>
      </div>

      {error && <div className="alert error">{error}</div>}

      <section className="panel form-panel">
        <div className="panel-header">
          <div>
            <h3>{editingId ? "Edit attendance" : "Record attendance"}</h3>
            <p>Use one record per employee and date.</p>
          </div>
          {editingId && <button className="secondary-button" type="button" onClick={resetForm}>Cancel edit</button>}
        </div>

        <form className="form-grid" onSubmit={submit}>
          <label>
            Employee
            <select value={form.employee_id} onChange={(e) => change("employee_id", e.target.value)} required>
              <option value="">Select employee</option>
              {employees.map((employee) => (
                <option key={employee.id} value={employee.id}>
                  {employee.employee_code || `#${employee.id}`} — {employee.first_name} {employee.last_name}
                </option>
              ))}
            </select>
          </label>

          <label>
            Date
            <input type="date" value={form.attendance_date} onChange={(e) => change("attendance_date", e.target.value)} required />
          </label>

          <label>
            Check in
            <input type="time" value={form.check_in} onChange={(e) => change("check_in", e.target.value)} />
          </label>

          <label>
            Check out
            <input type="time" value={form.check_out} onChange={(e) => change("check_out", e.target.value)} />
          </label>

          <label>
            Status
            <select value={form.status} onChange={(e) => change("status", e.target.value)} required>
              {STATUSES.map((status) => <option key={status}>{status}</option>)}
            </select>
          </label>

          <label className="field-wide">
            Remarks
            <textarea rows="3" value={form.remarks} onChange={(e) => change("remarks", e.target.value)} placeholder="Optional notes" />
          </label>

          <div className="form-actions field-wide">
            <button className="primary-button" disabled={saving}>
              {saving ? "Saving..." : editingId ? "Update record" : "Save attendance"}
            </button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h3>Attendance records</h3>
            <p>Filter records without leaving the page.</p>
          </div>
        </div>

        <div className="filter-grid">
          <select value={filters.employee_id} onChange={(e) => setFilters({ ...filters, employee_id: e.target.value })}>
            <option value="">All employees</option>
            {employees.map((employee) => (
              <option key={employee.id} value={employee.id}>{employee.first_name} {employee.last_name}</option>
            ))}
          </select>
          <select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
            <option value="">All statuses</option>
            {STATUSES.map((status) => <option key={status}>{status}</option>)}
          </select>
          <input type="date" value={filters.date} onChange={(e) => setFilters({ ...filters, date: e.target.value })} />
          <button className="secondary-button" onClick={load}>Apply filters</button>
        </div>

        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr><th>Employee</th><th>Date</th><th>Check in</th><th>Check out</th><th>Status</th><th>Remarks</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="7" className="empty-state">Loading attendance...</td></tr>
              ) : rows.length === 0 ? (
                <tr><td colSpan="7" className="empty-state">No attendance records found.</td></tr>
              ) : rows.map((row) => (
                <tr key={row.id}>
                  <td><strong>{employeeName(row.employee_id)}</strong></td>
                  <td>{row.attendance_date}</td>
                  <td>{formatTime(row.check_in)}</td>
                  <td>{formatTime(row.check_out)}</td>
                  <td><span className={`status-badge status-${String(row.status).toLowerCase()}`}>{row.status}</span></td>
                  <td>{row.remarks || "—"}</td>
                  <td className="actions">
                    <button className="text-button" onClick={() => startEdit(row)}>Edit</button>
                    <button className="text-button danger-text" onClick={() => remove(row.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
