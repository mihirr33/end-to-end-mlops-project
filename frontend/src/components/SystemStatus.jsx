    import { FaCircle } from "react-icons/fa";

function StatusItem({ name, status }) {
  return (
    <div className="status-item">
      <span>{name}</span>

      <div className="status-right">
        <FaCircle
          className={status ? "online" : "offline"}
        />

        <span>{status ? "Online" : "Offline"}</span>
      </div>
    </div>
  );
}

function SystemStatus({ health }) {
  return (
    <div className="system-card">

      <h2>System Status</h2>

      <StatusItem
        name="Backend API"
        status={health}
      />

      <StatusItem
        name="Prediction Model"
        status={health}
      />

      <StatusItem
        name="Prometheus"
        status={true}
      />

      <StatusItem
        name="Docker"
        status={true}
      />

      <StatusItem
        name="Kubernetes"
        status={true}
      />

    </div>
  );
}

export default SystemStatus;