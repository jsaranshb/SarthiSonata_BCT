import "bootstrap/dist/css/bootstrap.min.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./screens/Login";
import Dashboard from "./screens/Dashboard"; // Import other components if needed

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
}

export default App;
