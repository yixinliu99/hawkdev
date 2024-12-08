import React, { useEffect, useState } from 'react';

const ItemList = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await fetch('http://localhost:8081/items');
      const data = await response.json();
      setItems(data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  return (
    <div>
      <h2>Available Items</h2>
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.description} - {item.category}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ItemList;