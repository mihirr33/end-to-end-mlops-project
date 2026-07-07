function DashboardCard({ title, value, icon }) {
  return (
    <div className="dashboard-card">
      <div className="card-icon">{icon}</div>

      <div className="card-title">{title}</div>

      <div className="card-value">{value}</div>
    </div>
  );
}

export default DashboardCard;