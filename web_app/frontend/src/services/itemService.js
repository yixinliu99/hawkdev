import axios from 'axios';

const API_URL = 'http://localhost:5001/api/items'; 

const getItems = async () => {
  const response = await axios.get(API_URL, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`, 
    },
  });
  return response.data;
};

export default {
  getItems,
};
