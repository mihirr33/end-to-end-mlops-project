import { FaBrain, FaCircle } from "react-icons/fa";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-left">
        <FaBrain className="logo-icon" />

        <div>
          <h1>Ryvonexa AI</h1>
          <p>Enterprise Customer Intelligence Platform</p>
        </div>
      </div>

      <div className="navbar-right">
        <FaCircle className="status-dot" />
        <span>System Online</span>
      </div>
    </header>
  );
}

export default Navbar;