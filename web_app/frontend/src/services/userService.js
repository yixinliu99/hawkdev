import axios from 'axios';

const API_URL = 'http://localhost:5001/api'; 

const signup = async (userData) => {
  const response = await axios.post(`${API_URL}/users/signup`, userData);
  return response.data;
};

const login = async (userData) => {
  const response = await axios.post(`${API_URL}/users/login`, userData);
  console.log('Login successful');
  localStorage.setItem('authToken', response.data.token); 
  return response.data;
};

const logout = () => {
  localStorage.removeItem('authToken'); 
};


const getProfile = (token) => {
  return axios.get(`${API_URL}/users/profile`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

const updateProfile = (token, data) => {
  return axios.put(`${API_URL}/users/profile`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });
};


export default { signup, login, logout, getProfile, updateProfile };