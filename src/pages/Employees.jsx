import { useEffect, useState } from "react";
import { listDepartments } from "../services/departments";
import {
  createEmployee,
  deleteEmployee,
  listEmployees,
  updateEmployee,
} from "../services/employees";

const emptyForm = {
  employee_code: "", user_id: "", department_id: "", manager_id: "",
  first_name: "", last_name: "", phone: "", date_of_birth: "",
  date_of_joining: "", designation: "", employment_status: "ACTIVE",
};

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [search, setSearch] = useState("");
  const [departmentId, setDepartmentId] = useState("");
  const [activeOnly, setActiveOnly] = useState(true);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function loadData() {
    setLoading(true);
    try {
      setError("");
      const [employeeData, departmentData] = await Promise.all([
        listEmployees({
          skip: 0, limit: 100, search: search || undefined,
          department_id: departmentId || undefined, active_only: activeOnly,
        }),
        listDepartments(),
      ]);
      setEmployees(employeeData);
      setDepartments(departmentData);
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load employees.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadData(); }, [search, departmentId, activeOnly]);

  function handleChange(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function startEdit(employee) {
    setEditingId(employee.id);
    setForm({
      employee_code: employee.employee_code || "",
      user_id: employee.user_id ?? "",
      department_id: employee.department_id ?? "",
      manager_id: employee.manager_id ?? "",
      first_name: employee.first_name || "",
      last_name: employee.last_name || "",
      phone: employee.phone || "",
      date_of_birth: employee.date_of_birth || "",
      date_of_joining: employee.date_of_joining || "",
      designation: employee.designation || "",
      employment_status: employee.employment_status || "ACTIVE",
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      const payload = {
        ...form,
        user_id: Number(form.user_id),
        department_id: Number(form.department_id),
        manager_id: form.manager_id ? Number(form.manager_id) : null,
        date_of_birth: form.date_of_birth || null,
      };
      if (editingId) {
        const { employee_code, user_id, ...updatePayload } = payload;
        await updateEmployee(editingId, updatePayload);
      } else {
        await createEmployee(payload);
      }
      cancelEdit();
      await loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not save employee.");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this employee?")) return;
    try {
      setError("");
      await deleteEmployee(id);
      await loadData();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not delete employee.");
    }
  }

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <h1>Employees</h1>
          <p>Manage employee records and assignments.</p>
        </div>
      </div>

      <section className="content-card">
        <h2>{editingId ? "Edit employee" : "Add employee"}</h2>
        <form onSubmit={handleSubmit} className="employee-form">
          {!editingId && <>
            <label>Employee code
              <input name="employee_code" value={form.employee_code}
                onChange={handleChange} maxLength={30} required />
            </label>
            <label>User ID
              <input name="user_id" type="number" min="1" value={form.user_id}
                onChange={handleChange} required />
            </label>
          </>}

          <label>First name
            <input name="first_name" value={form.first_name}
              onChange={handleChange} maxLength={100} required />
          </label>
          <label>Last name
            <input name="last_name" value={form.last_name}
              onChange={handleChange} maxLength={100} required />
          </label>
          <label>Department
            <select name="department_id" value={form.department_id}
              onChange={handleChange} required>
              <option value="">Select department</option>
              {departments.map((department) => (
                <option key={department.id} value={department.id}>{department.name}</option>
              ))}
            </select>
          </label>
          <label>Manager ID
            <input name="manager_id" type="number" min="1" value={form.manager_id}
              onChange={handleChange} />
          </label>
          <label>Phone
            <input name="phone" value={form.phone} onChange={handleChange} maxLength={30} />
          </label>
          <label>Date of birth
            <input name="date_of_birth" type="date" value={form.date_of_birth}
              onChange={handleChange} />
          </label>
          <label>Date of joining
            <input name="date_of_joining" type="date" value={form.date_of_joining}
              onChange={handleChange} required />
          </label>
          <label>Designation
            <input name="designation" value={form.designation}
              onChange={handleChange} maxLength={100} required />
          </label>
          <label>Employment status
            <select name="employment_status" value={form.employment_status}
              onChange={handleChange}>
              <option value="ACTIVE">ACTIVE</option>
              <option value="INACTIVE">INACTIVE</option>
              <option value="ON_LEAVE">ON_LEAVE</option>
              <option value="TERMINATED">TERMINATED</option>
            </select>
          </label>

          {error && <p className="form-error form-wide">{error}</p>}
          <div className="form-actions form-wide">
            <button className="primary-button" disabled={saving}>
              {saving ? "Saving..." : editingId ? "Update" : "Add employee"}
            </button>
            {editingId && <button type="button" className="secondary-button"
              onClick={cancelEdit}>Cancel</button>}
          </div>
        </form>
      </section>

      <section className="content-card">
        <div className="filter-row">
          <input placeholder="Search employees..." value={search}
            onChange={(event) => setSearch(event.target.value)} />
          <select value={departmentId}
            onChange={(event) => setDepartmentId(event.target.value)}>
            <option value="">All departments</option>
            {departments.map((department) => (
              <option key={department.id} value={department.id}>{department.name}</option>
            ))}
          </select>
          <label className="checkbox-label">
            <input type="checkbox" checked={activeOnly}
              onChange={(event) => setActiveOnly(event.target.checked)} />
            Active only
          </label>
        </div>

        <h2>Employee list</h2>
        {loading ? <p>Loading employees...</p> :
          employees.length === 0 ? <p>No employees found.</p> :
          <div className="table-wrapper">
            <table className="data-table">
              <thead><tr>
                <th>Code</th><th>Name</th><th>Designation</th>
                <th>Department</th><th>Status</th><th>Actions</th>
              </tr></thead>
              <tbody>
                {employees.map((employee) => {
                  const department = departments.find(
                    (item) => item.id === employee.department_id
                  );
                  return <tr key={employee.id}>
                    <td>{employee.employee_code}</td>
                    <td>{employee.first_name} {employee.last_name}</td>
                    <td>{employee.designation}</td>
                    <td>{department?.name || employee.department_id}</td>
                    <td>{employee.employment_status}</td>
                    <td className="table-actions">
                      <button onClick={() => startEdit(employee)}>Edit</button>
                      <button onClick={() => handleDelete(employee.id)}>Delete</button>
                    </td>
                  </tr>;
                })}
              </tbody>
            </table>
          </div>}
      </section>
    </main>
  );
}
