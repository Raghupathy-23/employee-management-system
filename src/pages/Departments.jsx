import { useEffect, useState } from "react";
import {
  createDepartment,
  deleteDepartment,
  listDepartments,
  updateDepartment,
} from "../services/departments";

const emptyForm = { name: "", description: "", is_active: true };

export default function Departments() {
  const [departments, setDepartments] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function loadDepartments() {
    setLoading(true);
    try {
      setError("");
      setDepartments(await listDepartments());
    } catch (err) {
      setError(err.response?.data?.detail || "Could not load departments.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDepartments();
  }, []);

  function handleChange(event) {
    const { name, value, type, checked } = event.target;
    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  function startEdit(department) {
    setEditingId(department.id);
    setForm({
      name: department.name || "",
      description: department.description || "",
      is_active: department.is_active,
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
      if (editingId) {
        await updateDepartment(editingId, form);
      } else {
        await createDepartment(form);
      }
      cancelEdit();
      await loadDepartments();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not save department.");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete this department?")) return;
    try {
      setError("");
      await deleteDepartment(id);
      await loadDepartments();
    } catch (err) {
      setError(err.response?.data?.detail || "Could not delete department.");
    }
  }

  return (
    <main className="page">
      <div className="page-header">
        <div>
          <h1>Departments</h1>
          <p>Manage company departments.</p>
        </div>
      </div>

      <section className="content-card">
        <h2>{editingId ? "Edit department" : "Add department"}</h2>
        <form onSubmit={handleSubmit} className="data-form">
          <label>
            Name
            <input name="name" value={form.name} onChange={handleChange}
              maxLength={100} required />
          </label>
          <label>
            Description
            <input name="description" value={form.description}
              onChange={handleChange} maxLength={255} />
          </label>
          <label className="checkbox-label">
            <input type="checkbox" name="is_active" checked={form.is_active}
              onChange={handleChange} />
            Active
          </label>
          {error && <p className="form-error">{error}</p>}
          <div className="form-actions">
            <button className="primary-button" disabled={saving}>
              {saving ? "Saving..." : editingId ? "Update" : "Add department"}
            </button>
            {editingId && (
              <button type="button" className="secondary-button" onClick={cancelEdit}>
                Cancel
              </button>
            )}
          </div>
        </form>
      </section>

      <section className="content-card">
        <h2>Department list</h2>
        {loading ? <p>Loading departments...</p> :
          departments.length === 0 ? <p>No departments found.</p> :
          <div className="table-wrapper">
            <table className="data-table">
              <thead><tr>
                <th>Name</th><th>Description</th><th>Status</th><th>Actions</th>
              </tr></thead>
              <tbody>
                {departments.map((department) => (
                  <tr key={department.id}>
                    <td>{department.name}</td>
                    <td>{department.description || "—"}</td>
                    <td>{department.is_active ? "Active" : "Inactive"}</td>
                    <td className="table-actions">
                      <button onClick={() => startEdit(department)}>Edit</button>
                      <button onClick={() => handleDelete(department.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>}
      </section>
    </main>
  );
}
