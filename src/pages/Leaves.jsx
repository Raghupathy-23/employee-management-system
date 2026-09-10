import { useEffect, useState } from "react";
import {
  approveLeave,
  createLeave,
  deleteLeave,
  listLeaves,
  rejectLeave,
  updateLeave,
} from "../services/leaves";
import { listEmployees } from "../services/employees";
import RoleGate, { useCurrentRole } from "../components/RoleGate";
import "../styles/hr.css";

const TYPES = ["ANNUAL", "SICK", "CASUAL", "UNPAID", "OTHER"];
const STATUSES = ["PENDING", "APPROVED", "REJECTED", "CANCELLED"];

const emptyForm = {
  employee_id: "",
  leave_type: "ANNUAL",
  start_date: "",
  end_date: "",
  reason: "",
};

export default function Leaves() {
  const [rows, setRows] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [filters, setFilters] = useState({ employee_id: "", status: "" });
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const role = useCurrentRole();
  const canApprove = ["ADMIN", "HR", "HR_MANAGER", "MANAGER"].includes(role);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const params = {};
      if (filters.employee_id) params.employee_id = filters.employee_id;
      if (filters.status) params.status = filters.status;
      const [leaveData, employeeData] = await Promise.all([
        listLeaves(params),
        listEmployees({ limit: 100 }),
      ]);
      setRows(Array.isArray(leaveData) ? leaveData : leaveData.items || []);
      setEmployees(Array.isArray(employeeData) ? employeeData : employeeData.items || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load leave requests.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  function employeeName(id) {
    const employee = employees.find((item) => item.id === id);
    return employee ? `${employee.first_name || ""} ${employee.last_name || ""}`.trim() : `Employee #${id}`;
  }

  function change(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function startEdit(row) {
    setEditingId(row.id);
    setForm({
      employee_id: row.employee_id ?? "",
      leave_type: row.leave_type || "ANNUAL",
      start_date: row.start_date || "",
      end_date: row.end_date || "",
      reason: row.reason || "",
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
      const payload = { ...form, employee_id: Number(form.employee_id) };
      if (editingId) await updateLeave(editingId, payload);
      else await createLeave(payload);
      resetForm();
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to save leave request.");
    } finally {
      setSaving(false);
    }
  }

  async function remove(id) {
    if (!window.confirm("Delete this leave request?")) return;
    try {
      await deleteLeave(id);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete leave request.");
    }
  }

  async function decide(id, action) {
    const comment = window.prompt(`${action === "approve" ? "Approval" : "Rejection"} comment (optional):`) || "";
    try {
      if (action === "approve") await approveLeave(id, comment);
      else await rejectLeave(id, comment);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || `Unable to ${action} leave request.`);
    }
  }

  return (
    <div className="hr-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">HR Operations</p>
          <h2>Leave Management</h2>
          <p className="page-subtitle">Submit, review, and track employee leave requests.</p>
        </div>
        <div className="stat-pill">{rows.length} requests</div>
      </div>

      {error && <div className="alert error">{error}</div>}

      <section className="panel form-panel">
        <div className="panel-header">
          <div>
            <h3>{editingId ? "Edit leave request" : "New leave request"}</h3>
            <p>Pending requests can be edited or removed.</p>
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
            Leave type
            <select value={form.leave_type} onChange={(e) => change("leave_type", e.target.value)} required>
              {TYPES.map((type) => <option key={type}>{type}</option>)}
            </select>
          </label>
          <label>
            Start date
            <input type="date" value={form.start_date} onChange={(e) => change("start_date", e.target.value)} required />
          </label>
          <label>
            End date
            <input type="date" value={form.end_date} onChange={(e) => change("end_date", e.target.value)} required />
          </label>
          <label className="field-wide">
            Reason
            <textarea rows="3" value={form.reason} onChange={(e) => change("reason", e.target.value)} placeholder="Reason for leave" required />
          </label>
          <div className="form-actions field-wide">
            <button className="primary-button" disabled={saving}>{saving ? "Saving..." : editingId ? "Update request" : "Submit request"}</button>
          </div>
        </form>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h3>Leave requests</h3>
            <p>Review request status and approval actions.</p>
          </div>
        </div>

        <div className="filter-grid">
          <select value={filters.employee_id} onChange={(e) => setFilters({ ...filters, employee_id: e.target.value })}>
            <option value="">All employees</option>
            {employees.map((employee) => <option key={employee.id} value={employee.id}>{employee.first_name} {employee.last_name}</option>)}
          </select>
          <select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
            <option value="">All statuses</option>
            {STATUSES.map((status) => <option key={status}>{status}</option>)}
          </select>
          <button className="secondary-button" onClick={load}>Apply filters</button>
        </div>

        <div className="table-wrap">
          <table className="data-table">
            <thead>
              <tr><th>Employee</th><th>Type</th><th>Dates</th><th>Reason</th><th>Status</th><th>Approval</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="7" className="empty-state">Loading leave requests...</td></tr>
              ) : rows.length === 0 ? (
                <tr><td colSpan="7" className="empty-state">No leave requests found.</td></tr>
              ) : rows.map((row) => (
                <tr key={row.id}>
                  <td><strong>{employeeName(row.employee_id)}</strong></td>
                  <td>{row.leave_type}</td>
                  <td>{row.start_date}<br />to {row.end_date}</td>
                  <td className="reason-cell">{row.reason || "—"}</td>
                  <td><span className={`status-badge status-${String(row.status).toLowerCase()}`}>{row.status}</span></td>
                  <td>{row.approval_comment || "—"}</td>
                  <td className="actions">
                    {row.status === "PENDING" && (
                      <>
                        <button className="text-button" onClick={() => startEdit(row)}>Edit</button>
                        <button className="text-button danger-text" onClick={() => remove(row.id)}>Delete</button>
                      </>
                    )}
                    {canApprove && row.status === "PENDING" && (
                      <>
                        <button className="text-button" onClick={() => decide(row.id, "approve")}>Approve</button>
                        <button className="text-button danger-text" onClick={() => decide(row.id, "reject")}>Reject</button>
                      </>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {!canApprove && (
          <div className="info-note">Approval controls are available to authorized HR/management roles.</div>
        )}
      </section>
    </div>
  );
}
