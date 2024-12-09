import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

const Bidding = () => {
  const [items, setItems] = useState([]);
  const navigate = useNavigate();
  const { user_id } = useParams();

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await fetch('http://localhost:8081/items');
        const data = await response.json(); 
        console.log('Fetched items:', data); // Log the fetched data
        setItems(data); // Set the items state with the fetched data
      } catch (error) {
        console.error('Failed to fetch items', error);
      }
    };

    fetchItems();
  }, []);

  return (
    <div>
      <h2>Items for Bidding</h2>
      <div>
        {items.length === 0 ? (
          <p>No items available for bidding</p>
        ) : (
          items.map((item) => (
            <div key={item._id}>
              <h3>{item.description}</h3>
              <p>{item.category}</p>
              <p>${item.starting_price}</p>
              <button onClick={() => navigate(`/bid/${item._id}`)}>Place Bid</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Bidding;