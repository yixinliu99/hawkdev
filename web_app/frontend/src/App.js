import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'font-awesome/css/font-awesome.min.css';
import Signup from './components/Signup';
import Login from './components/Login';
import Bidding from './components/Bidding';
import Navbar from './components/Navbar';

function App() {
  const token = localStorage.getItem('token'); // Check if a token exists

  return (
    <Router>
      {/* Only show Navbar if there's a valid token */}
      {token && <Navbar />}  {/* Conditionally render Navbar */}
      <div className="App">
        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/bidding" element={<Bidding />} />
          {/* Add other routes as necessary */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
