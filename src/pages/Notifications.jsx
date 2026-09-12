import { useEffect, useState } from "react";
import {
  listNotifications,
  markAllNotificationsRead,
  markNotificationRead,
} from "../services/notifications";
import "../styles/hr.css";

export default function Notifications() {
  const [items, setItems] = useState([]);
  const [unreadOnly, setUnreadOnly] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await listNotifications({ limit: 100, unread_only: unreadOnly });
      setItems(data.items || []);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load notifications.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [unreadOnly]);

  async function read(id) {
    try {
      await markNotificationRead(id);
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update notification.");
    }
  }

  async function markAllRead() {
    try {
      await markAllNotificationsRead();
      await load();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update notifications.");
    }
  }

  return (
    <div className="hr-page">
      <div className="page-heading">
        <div>
          <p className="eyebrow">System</p>
          <h2>Notifications</h2>
          <p className="page-subtitle">Review alerts and mark completed notifications as read.</p>
        </div>
        <div className="form-actions">
          <label className="checkbox-label">
            <input type="checkbox" checked={unreadOnly} onChange={(e) => setUnreadOnly(e.target.checked)} />
            Unread only
          </label>
          <button className="secondary-button" type="button" onClick={markAllRead}>Mark all read</button>
        </div>
      </div>

      {error && <div className="alert error">{error}</div>}
      <section className="panel">
        {loading ? (
          <p>Loading notifications...</p>
        ) : items.length === 0 ? (
          <p>No notifications found.</p>
        ) : (
          <div className="notification-page-list">
            {items.map((item) => (
              <article key={item.id} className={`notification-card ${item.is_read ? "read" : "unread"}`}>
                <div>
                  <div className="notification-card-title">{item.title}</div>
                  <p>{item.message}</p>
                  <small>{new Date(item.created_at).toLocaleString()}</small>
                </div>
                {!item.is_read && (
                  <button className="secondary-button" type="button" onClick={() => read(item.id)}>
                    Mark read
                  </button>
                )}
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
