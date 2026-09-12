import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  getUnreadNotificationCount,
  listNotifications,
  markAllNotificationsRead,
  markNotificationRead,
} from "../services/notifications";

export default function NotificationBell() {
  const [open, setOpen] = useState(false);
  const [items, setItems] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    try {
      const [countData, listData] = await Promise.all([
        getUnreadNotificationCount(),
        listNotifications({ limit: 5 }),
      ]);
      setUnreadCount(countData.unread_count || 0);
      setItems(listData.items || []);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load notifications.");
    }
  }, []);

  useEffect(() => {
    refresh();
    const timer = window.setInterval(refresh, 30000);
    return () => window.clearInterval(timer);
  }, [refresh]);

  async function read(id) {
    try {
      await markNotificationRead(id);
      await refresh();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update notification.");
    }
  }

  async function markAllRead() {
    try {
      await markAllNotificationsRead();
      await refresh();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update notifications.");
    }
  }

  return (
    <div className="notification-bell-wrap">
      <button
        className="notification-bell"
        type="button"
        aria-label="Notifications"
        onClick={() => setOpen((value) => !value)}
      >
        <span aria-hidden="true">🔔</span>
        {unreadCount > 0 && <span className="notification-badge">{unreadCount > 99 ? "99+" : unreadCount}</span>}
      </button>

      {open && (
        <div className="notification-popover">
          <div className="notification-popover-header">
            <strong>Notifications</strong>
            <button type="button" className="text-button" onClick={markAllRead} disabled={!unreadCount}>
              Mark all read
            </button>
          </div>
          {error && <div className="notification-error">{error}</div>}
          {items.length === 0 ? (
            <div className="notification-empty">No notifications.</div>
          ) : (
            <div className="notification-list">
              {items.map((item) => (
                <button
                  key={item.id}
                  type="button"
                  className={`notification-item ${item.is_read ? "read" : "unread"}`}
                  onClick={() => read(item.id)}
                >
                  <span className="notification-title">{item.title}</span>
                  <span className="notification-message">{item.message}</span>
                </button>
              ))}
            </div>
          )}
          <Link className="notification-view-all" to="/notifications" onClick={() => setOpen(false)}>
            View all notifications
          </Link>
        </div>
      )}
    </div>
  );
}
