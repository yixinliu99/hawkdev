import axios from 'axios';

const API_URL = 'http://localhost:5001/api'; 

const signup = async (userData) => {
  const response = await axios.post(`${API_URL}/users/signup`, userData);
  return response.data;
};

const login = async (userData) => {
  const response = await axios.post(`${API_URL}/users/login`, userData);
  localStorage.setItem('authToken', response.data.token); 
  return response.data;
};

const logout = () => {
  localStorage.removeItem('authToken'); 
};

export default { signup, login, logout };
