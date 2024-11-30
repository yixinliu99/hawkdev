import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const Navbar = () => {
  const token = localStorage.getItem('token'); 
  const navigate = useNavigate();
  const location = useLocation(); // Get the current location

  // Paths where the Navbar should not be displayed
  const excludedPaths = ['/login', '/signup'];

  // Check if the current path is in the excluded paths
  if (excludedPaths.includes(location.pathname)) {
    return null; // Do not render Navbar
  }

  const handleLogout = () => {
    localStorage.removeItem('token'); // Remove token from localStorage
    navigate('/login'); // Redirect to login page
  };

  return (
    <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 20px', backgroundColor: '#f8f9fa' }}>
      <div>Logo</div>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <Link to="/profile" style={{ margin: '0 10px' }}>
          <i className="fas fa-user"></i> Profile
        </Link>
        <Link to="/cart" style={{ margin: '0 10px' }}>
          <i className="fas fa-shopping-cart"></i> Cart
        </Link>
        <Link to="/sell-item" style={{ margin: '0 10px' }}>
          <i className="fas fa-plus-circle"></i> Sell Item
        </Link>
        <button onClick={handleLogout} style={{ margin: '0 10px' }}>
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
