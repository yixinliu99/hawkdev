import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import 'font-awesome/css/font-awesome.min.css';
import Signup from './components/Signup';
import Login from './components/Login';
import Bidding from './components/Bidding';
import Profile from './components/Profile';
import Navbar from './components/Navbar';
import Cart from './components/Cart';
import SellItem from './components/SellItem';
import ItemList from './components/ItemList'; // Import the new component

function App() {
  const token = localStorage.getItem('token'); // Check if a token exists

  return (
    <Router>
      <Navbar />  
      <div className="App">
        <Routes>
          <Route path="/signup" element={<Signup />} />
          <Route path="/profile/:user_id" element={<Profile />} />
          <Route path="/" element={<Login />} />
          <Route path="/bidding/:user_id" element={<Bidding />} />
          <Route path="/cart/:user_id" element={<Cart />}/>
          <Route path="/sell-item/:user_id" element={<SellItem />}/>
          <Route path="/items" element={<ItemList />} /> {/* Add the new route */}
          {/* Add other routes as necessary */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;