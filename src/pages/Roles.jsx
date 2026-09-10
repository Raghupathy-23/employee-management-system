import { useEffect, useState } from "react";
import { createRole, deleteRole, listRoles, updateRole } from "../services/roles";
import RoleGate from "../components/RoleGate";
import "../styles/hr.css";

const emptyForm = { name: "", description: "" };

function RolesContent() {
  const [rows, setRows] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await listRoles();
      setRows(Array.isArray(data) ? data : data.items || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load roles.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  function change(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function startEdit(role) {
    setEditingId(role.id);
    setForm({ name: role.name || "", description: role.description || "" });
  }

  function reset() {
    setEditingId(null);
    setForm(emptyForm);
  }

  async function submit(event) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      if (editingId) await updateRole(editingId, form);
      else await createRole(form);
      reset();
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to save role.");
    } finally {
      setSaving(false);
    }
  }

  async function remove(id) {
    if (!window.confirm("Delete this role? Users assigned to the role may prevent deletion.")) return;
    try {
      await deleteRole(id);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete role.");
    }
  }

  return (
    <div className="hr-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">Administration</p>
          <h2>Roles</h2>
          <p className="page-subtitle">Manage the application roles used for access control.</p>
        </div>
        <div className="stat-pill">{rows.length} roles</div>
      </div>

      {error && <div className="alert error">{error}</div>}

      <div className="two-column">
        <section className="panel form-panel">
          <div className="panel-header">
            <div>
              <h3>{editingId ? "Edit role" : "Create role"}</h3>
              <p>Keep role names short and descriptive.</p>
            </div>
            {editingId && <button className="secondary-button" type="button" onClick={reset}>Cancel</button>}
          </div>

          <form className="stack-form" onSubmit={submit}>
            <label>
              Role name
              <input value={form.name} onChange={(e) => change("name", e.target.value.toUpperCase())} placeholder="HR_MANAGER" required />
            </label>
            <label>
              Description
              <textarea rows="5" value={form.description} onChange={(e) => change("description", e.target.value)} placeholder="What can this role do?" />
            </label>
            <button className="primary-button" disabled={saving}>{saving ? "Saving..." : editingId ? "Update role" : "Create role"}</button>
          </form>
        </section>

        <section className="panel">
          <div className="panel-header">
            <div>
              <h3>Available roles</h3>
              <p>Roles currently configured in the system.</p>
            </div>
          </div>

          <div className="role-list">
            {loading ? (
              <div className="empty-state">Loading roles...</div>
            ) : rows.length === 0 ? (
              <div className="empty-state">No roles found.</div>
            ) : rows.map((role) => (
              <article className="role-card" key={role.id}>
                <div>
                  <div className="role-title">{role.name}</div>
                  <p>{role.description || "No description provided."}</p>
                </div>
                <div className="actions">
                  <button className="text-button" onClick={() => startEdit(role)}>Edit</button>
                  <button className="text-button danger-text" onClick={() => remove(role.id)}>Delete</button>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export default function Roles() {
  return (
    <RoleGate
      allowedRoles={["ADMIN"]}
      fallback={
        <div className="hr-page">
          <section className="panel access-denied">
            <h2>Access restricted</h2>
            <p>Role administration is available only to administrators.</p>
          </section>
        </div>
      }
    >
      <RolesContent />
    </RoleGate>
  );
}
