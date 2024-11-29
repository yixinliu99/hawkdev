import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Navbar = () => {
  const token = localStorage.getItem('token'); 
  const navigate = useNavigate();

  // If there's no token, don't render Navbar
  if (!token) {
    return null;
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
