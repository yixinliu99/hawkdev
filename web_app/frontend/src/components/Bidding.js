import React, { useEffect, useState } from 'react';
import itemService from '../services/itemService'; 
import { useNavigate } from 'react-router-dom';
import Navbar from './Navbar'; 

const Bidding = () => {
  const [items, setItems] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await itemService.getItems(); 
        setItems(response.data);
      } catch (error) {
        console.error('Failed to fetch items', error);
      }
    };

    fetchItems();
  }, []);

  return (
    <div>
      {/*<Navbar />  Include the Navbar here */}
      <h2>Items for Bidding</h2>
      <div>
        {items.length === 0 ? (
          <p>No items available for bidding</p>
        ) : (
          items.map((item) => (
            <div key={item.id}>
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <button onClick={() => navigate(`/bid/${item.id}`)}>Place Bid</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Bidding;
