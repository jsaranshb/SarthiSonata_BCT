import React, { useEffect, useState } from "react";
import Loader from "../components/Loader";
import NavBar from "../components/navBar";
import SideBar from "../components/sideBar";
import Footer from "../components/Footer";
import "../assets/css/dashboard.css";

const Dashboard = () => {
  const [userData, setUserData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/dashboard/business_calling/",
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          setUserData(data);
        } else {
          console.log("Failed to fetch data");
        }
      } catch (error) {
        console.error("Error:", error);
      } finally {
        setIsLoading(false);
        setIsButtonDisabled(false);
      }
    };

    // Get data from local storage or perform fetch
    const localUserData = JSON.parse(localStorage.getItem("user_data"));
    if (localUserData) {
      setUserData(localUserData);
    } else {
      fetchData();
    }
  }, []);

  return (
    <>
      <NavBar />
      <SideBar />
      <div className="main-content">
        <h2>Main Content</h2>
        <p>This is where the main content of the page will go.</p>
        {userData ? <pre>{JSON.stringify(userData, null, 2)}</pre> : <Loader />}
      </div>
      <Footer />
    </>
  );
};

export default Dashboard;
