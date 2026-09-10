import { useEffect, useState } from "react";
import api from "../services/api";

export default function Dashboard() {
  const [system, setSystem] = useState(null);
  const [database, setDatabase] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadSystemInfo() {
      try {
        const [systemResponse, databaseResponse] = await Promise.all([
          api.get("/system/info"),
          api.get("/system/database"),
        ]);

        setSystem(systemResponse.data);
        setDatabase(databaseResponse.data);
      } catch {
        setError("Could not load backend system information.");
      }
    }

    loadSystemInfo();
  }, []);

  return (
    <div>
      <div className="welcome">
        <div>
          <p className="eyebrow">Overview</p>
          <h2>Welcome back</h2>
          <p>Frontend Phase 1–3 is connected to your FastAPI backend.</p>
        </div>
      </div>

      {error && <div className="alert">{error}</div>}

      <div className="stats-grid">
        <article className="stat-card">
          <span>Backend</span>
          <strong>{system ? "Connected" : "Checking..."}</strong>
          <small>FastAPI API</small>
        </article>

        <article className="stat-card">
          <span>Database</span>
          <strong>{database ? "Connected" : "Checking..."}</strong>
          <small>MySQL status endpoint</small>
        </article>

        <article className="stat-card">
          <span>Authentication</span>
          <strong>Active</strong>
          <small>JWT bearer token</small>
        </article>
      </div>

      <section className="info-card">
        <div>
          <p className="eyebrow">System information</p>
          <h3>API connection</h3>
        </div>

        <dl className="info-list">
          <div>
            <dt>API status</dt>
            <dd>{system ? "Online" : "Checking..."}</dd>
          </div>
          <div>
            <dt>Database status</dt>
            <dd>{database ? "Online" : "Checking..."}</dd>
          </div>
        </dl>
      </section>
    </div>
  );
}