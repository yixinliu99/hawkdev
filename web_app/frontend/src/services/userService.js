import axios from 'axios';

const API_URL = 'http://localhost:5001/api'; 

const signup = async (userData) => {
  const response = await axios.post(`${API_URL}/users/signup`, userData);
  return response.data;
};

const login = async (userData) => {
  const response = await axios.post(`${API_URL}/users/`, userData);
  console.log('Login successful');
  localStorage.setItem('authToken', response.data.token); 
  localStorage.setItem('userId', response.data.user_id)
  return response.data;
};

const logout = () => {
  localStorage.removeItem('authToken'); 
};


const getProfile = (token, userId) => {
  return axios.get(`${API_URL}/users/profile/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

const updateProfile = (token, userId, data) => {
  return axios.put(`${API_URL}/users/profile/${userId}`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

const getCart = async (userId) => {
  const token = localStorage.getItem('authToken');
  const headers = { Authorization: `Bearer ${token}` };
  const response = await axios.get(`${API_URL}/users/cart/${userId}`, { headers });
  return response.data;
};

// Remove an item from the cart
const removeFromCart = async (userId, itemId) => {
  const token = localStorage.getItem('authToken');
  const headers = { Authorization: `Bearer ${token}` };
  const response = await axios.delete(`${API_URL}/users/cart/${userId}`, {
    headers,
    data: { item_id: itemId }, // Ensure backend handles this
  });
  return response.data;
};

export default { signup, login, logout, getProfile, updateProfile, getCart, removeFromCart };