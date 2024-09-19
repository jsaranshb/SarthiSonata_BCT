import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Base64 } from "js-base64"; // For encoding the password
import Loader from "../components/Loader";
import "../assets/css/login.css";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);
  const navigate = useNavigate();

  // This will be required to add the CSRF token to the request
  const getCSRFToken = () => {
    let csrfToken = null;
    const cookies = document.cookie.split(";");
    cookies.forEach((cookie) => {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        csrfToken = value;
      }
    });
    return csrfToken;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setIsButtonDisabled(true);

    // Encode password
    const encodedPassword = Base64.encode(password);

    // Prepare the data to be sent in the request
    const data = {
      username: username,
      password: encodedPassword,
    };

    // CSRF token (important for Django POST requests)
    const csrfToken = getCSRFToken();

    // Send the POST request to the Django backend
    try {
      const response = await fetch("http://127.0.0.1:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken, // Add CSRF token to the header
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const data = await response.json();

        // Save tokens to localStorage
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        // Redirect to another page
        navigate("/dashboard"); // Redirect to the desired page
      } else {
        const errorData = await response.json();
        const errorMessage = errorData.error || "An unknown error occurred";
        alert(errorMessage); // Show alert with error message
      }
    } catch (error) {
      alert("Error fetching user data"); // Show alert for unexpected errors
    } finally {
      setIsLoading(false);
      setIsButtonDisabled(false);
    }
  };

  return (
    <div className="container login-container">
      {isLoading && <Loader />} {/* Show loader if isLoading is true */}
      <div className="row align-items-center">
        <div className="col-md-6">
          <img
            src="/images/login-page-img.png"
            alt="Background"
            className="img-fluid background-image"
          />
        </div>
        <div className="col-md-6">
          <div className="login-box">
            <h2 className="text-center mb-4">Login To Sarthi</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-group mb-3">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  className="form-control"
                  id="username"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </div>
              <div className="form-group mb-4">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  className="form-control"
                  id="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
              <button type="submit" className="btn btn-primary w-100">
                Sign In
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
