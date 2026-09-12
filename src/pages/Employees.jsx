import { useEffect, useState } from "react";
import { listDepartments } from "../services/departments";
import {
  createEmployee,
  deleteEmployee,
  listEmployees,
  updateEmployee,
} from "../services/employees";

const emptyForm = {
  employee_code: "",
  user_id: "",
  department_id: "",
  manager_id: "",
  first_name: "",
  last_name: "",
  phone: "",
  date_of_birth: "",
  date_of_joining: "",
  designation: "",
  employment_status: "ACTIVE",
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
          skip: 0,
          limit: 100,
          search: search || undefined,
          department_id: departmentId || undefined,
          active_only: activeOnly,
        }),
        listDepartments(),
      ]);

      setEmployees(employeeData);
      setDepartments(departmentData);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Could not load employees."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [search, departmentId, activeOnly]);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
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
      employment_status:
        employee.employment_status || "ACTIVE",
    });

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(emptyForm);
    setError("");
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
        manager_id: form.manager_id
          ? Number(form.manager_id)
          : null,
        date_of_birth: form.date_of_birth || null,
      };

      if (editingId) {
        const {
          employee_code,
          user_id,
          ...updatePayload
        } = payload;

        await updateEmployee(
          editingId,
          updatePayload
        );
      } else {
        await createEmployee(payload);
      }

      cancelEdit();
      await loadData();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Could not save employee."
      );
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id) {
    if (
      !window.confirm(
        "Are you sure you want to delete this employee?"
      )
    ) {
      return;
    }

    try {
      setError("");

      await deleteEmployee(id);
      await loadData();
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Could not delete employee."
      );
    }
  }

  function getDepartmentName(departmentId) {
    const department = departments.find(
      (item) => item.id === departmentId
    );

    return department?.name || "—";
  }

  function getInitials(employee) {
    return `${employee.first_name?.charAt(0) || ""}${employee.last_name?.charAt(0) || ""}`
      .toUpperCase();
  }

  function formatStatus(status) {
    return status
      ?.replaceAll("_", " ")
      .toLowerCase()
      .replace(/\b\w/g, (char) => char.toUpperCase());
  }

  return (
    <main className="hr-page">

      {/* =====================================================
          PAGE HEADER
          ===================================================== */}

      <div className="page-heading">
        <div>
          <p className="eyebrow">HR MANAGEMENT</p>

          <h2>Employees</h2>

          <p className="page-subtitle">
            Manage employee records, assignments and employment status.
          </p>
        </div>

        <div className="stat-pill">
          {employees.length}{" "}
          {employees.length === 1
            ? "employee"
            : "employees"}
        </div>
      </div>


      {/* =====================================================
          ERROR
          ===================================================== */}

      {error && (
        <div className="alert error">
          {error}
        </div>
      )}


      {/* =====================================================
          EMPLOYEE FORM
          ===================================================== */}

      <section className="panel">

        <div className="panel-header">
          <div>
            <h3>
              {editingId
                ? "Edit employee"
                : "Add employee"}
            </h3>

            <p>
              {editingId
                ? "Update the employee's information below."
                : "Enter the employee information to create a new record."}
            </p>
          </div>
        </div>

        <form
          onSubmit={handleSubmit}
          className="form-grid"
        >

          {!editingId && (
            <>
              <label>
                Employee code

                <input
                  name="employee_code"
                  value={form.employee_code}
                  onChange={handleChange}
                  maxLength={30}
                  placeholder="EMP-001"
                  required
                />
              </label>

              <label>
                User ID

                <input
                  name="user_id"
                  type="number"
                  min="1"
                  value={form.user_id}
                  onChange={handleChange}
                  placeholder="User ID"
                  required
                />
              </label>
            </>
          )}

          <label>
            First name

            <input
              name="first_name"
              value={form.first_name}
              onChange={handleChange}
              maxLength={100}
              placeholder="First name"
              required
            />
          </label>

          <label>
            Last name

            <input
              name="last_name"
              value={form.last_name}
              onChange={handleChange}
              maxLength={100}
              placeholder="Last name"
              required
            />
          </label>

          <label>
            Department

            <select
              name="department_id"
              value={form.department_id}
              onChange={handleChange}
              required
            >
              <option value="">
                Select department
              </option>

              {departments.map((department) => (
                <option
                  key={department.id}
                  value={department.id}
                >
                  {department.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            Designation

            <input
              name="designation"
              value={form.designation}
              onChange={handleChange}
              maxLength={100}
              placeholder="e.g. Software Engineer"
              required
            />
          </label>

          <label>
            Manager ID

            <input
              name="manager_id"
              type="number"
              min="1"
              value={form.manager_id}
              onChange={handleChange}
              placeholder="Optional"
            />
          </label>

          <label>
            Phone

            <input
              name="phone"
              value={form.phone}
              onChange={handleChange}
              maxLength={30}
              placeholder="+91..."
            />
          </label>

          <label>
            Date of birth

            <input
              name="date_of_birth"
              type="date"
              value={form.date_of_birth}
              onChange={handleChange}
            />
          </label>

          <label>
            Date of joining

            <input
              name="date_of_joining"
              type="date"
              value={form.date_of_joining}
              onChange={handleChange}
              required
            />
          </label>

          <label>
            Employment status

            <select
              name="employment_status"
              value={form.employment_status}
              onChange={handleChange}
            >
              <option value="ACTIVE">
                Active
              </option>

              <option value="INACTIVE">
                Inactive
              </option>

              <option value="ON_LEAVE">
                On Leave
              </option>

              <option value="TERMINATED">
                Terminated
              </option>
            </select>
          </label>

          <div className="form-actions field-wide">

            {editingId && (
              <button
                type="button"
                className="secondary-button"
                onClick={cancelEdit}
                disabled={saving}
              >
                Cancel
              </button>
            )}

            <button
              type="submit"
              className="primary-button"
              disabled={saving}
            >
              {saving
                ? "Saving..."
                : editingId
                ? "Update employee"
                : "Add employee"}
            </button>

          </div>

        </form>
      </section>


      {/* =====================================================
          EMPLOYEE LIST
          ===================================================== */}

      <section className="panel">

        <div className="panel-header">
          <div>
            <h3>Employee directory</h3>

            <p>
              Search and manage employees in the organization.
            </p>
          </div>
        </div>


        {/* Filters */}

        <div className="filter-grid">

          <input
            placeholder="Search by name, code or designation..."
            value={search}
            onChange={(event) =>
              setSearch(event.target.value)
            }
          />

          <select
            value={departmentId}
            onChange={(event) =>
              setDepartmentId(event.target.value)
            }
          >
            <option value="">
              All departments
            </option>

            {departments.map((department) => (
              <option
                key={department.id}
                value={department.id}
              >
                {department.name}
              </option>
            ))}
          </select>

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={activeOnly}
              onChange={(event) =>
                setActiveOnly(event.target.checked)
              }
            />

            Active employees only
          </label>

          {(search || departmentId || !activeOnly) && (
            <button
              type="button"
              className="secondary-button"
              onClick={() => {
                setSearch("");
                setDepartmentId("");
                setActiveOnly(true);
              }}
            >
              Clear filters
            </button>
          )}

        </div>


        {/* Results */}

        {loading ? (
          <div className="empty-state">
            Loading employees...
          </div>
        ) : employees.length === 0 ? (
          <div className="empty-state">
            No employees found.
          </div>
        ) : (
          <div className="table-wrap">

            <table className="data-table">

              <thead>
                <tr>
                  <th>Employee</th>
                  <th>Code</th>
                  <th>Department</th>
                  <th>Designation</th>
                  <th>Joining Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>

                {employees.map((employee) => (
                  <tr key={employee.id}>

                    {/* Employee */}

                    <td>
                      <div className="employee-cell">

                        <div className="employee-avatar">
                          {getInitials(employee)}
                        </div>

                        <div>
                          <div className="employee-name">
                            {employee.first_name}{" "}
                            {employee.last_name}
                          </div>

                          <div className="employee-id">
                            ID #{employee.id}
                          </div>
                        </div>

                      </div>
                    </td>


                    {/* Code */}

                    <td>
                      <span className="employee-code">
                        {employee.employee_code}
                      </span>
                    </td>


                    {/* Department */}

                    <td>
                      {getDepartmentName(
                        employee.department_id
                      )}
                    </td>


                    {/* Designation */}

                    <td>
                      {employee.designation || "—"}
                    </td>


                    {/* Joining date */}

                    <td>
                      {employee.date_of_joining || "—"}
                    </td>


                    {/* Status */}

                    <td>
                      <span
                        className={`status-badge status-${employee.employment_status?.toLowerCase()}`}
                      >
                        {formatStatus(
                          employee.employment_status
                        )}
                      </span>
                    </td>


                    {/* Actions */}

                    <td>
                      <div className="actions">

                        <button
                          type="button"
                          className="text-button"
                          onClick={() =>
                            startEdit(employee)
                          }
                        >
                          Edit
                        </button>

                        <button
                          type="button"
                          className="text-button danger-text"
                          onClick={() =>
                            handleDelete(employee.id)
                          }
                        >
                          Delete
                        </button>

                      </div>
                    </td>

                  </tr>
                ))}

              </tbody>

            </table>

          </div>
        )}

      </section>

    </main>
  );
}