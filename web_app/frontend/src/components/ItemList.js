import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { itemWatchlistMatch } from '../services/userService';  // Import from the new service file

const ItemList = () => {
  const [items, setItems] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchAllItems(); // Fetch all items when the component mounts
  }, []);

  const fetchAllItems = async () => {
    try {
      // Fetch all items from the item microservice using axios
      const response = await axios.get('http://localhost:8081/items');
      const data = response.data;

      // Set the state with the fetched items
      setItems(data);

      // Check the fetched items with the user's watchlist
      await checkWithWatchlist(data);
    } catch (error) {
      console.error('Error fetching items:', error);
      setMessage('Error fetching items.');
    }
  };

  const checkWithWatchlist = async (allItems) => {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      setMessage('User not authenticated.');
      return;
    }

    try {
      // Prepare the watchlist criteria to be sent to the user microservice
      const watchlistCriteria = {
        keywords: allItems.map(item => item.keywords), // Assuming each item has 'keywords'
        categories: allItems.map(item => item.category), // Assuming each item has 'category'
      };

      // Get user's watchlist match information from the user microservice
      const watchlistResponse = await itemWatchlistMatch(userId, watchlistCriteria);

      // Ensure watchlistResponse is an array and contains items
      if (!Array.isArray(watchlistResponse) || watchlistResponse.length === 0) {
        setMessage('No items found in the watchlist.');
        return;
      }

      // Check each item if it matches the user's watchlist criteria
      allItems.forEach((item) => {
        const isMatch = watchlistResponse.some((watchlistItem) => 
          item.keywords.includes(watchlistItem.keyword) && 
          item.category === watchlistItem.category
        );

        if (isMatch) {
          console.log(`Match found for item: ${item.description}`);
          // Trigger a notification or email here (could call another service)
        }
      });
    } catch (error) {
      console.error('Error checking with watchlist:', error);
      setMessage('Error checking with watchlist.');
    }
  };

  return (
    <div>
      <h2>Available Items</h2>
      {message && <p>{message}</p>}
      <ul>
        {items.length === 0 ? (
          <p>No items available.</p>
        ) : (
          items.map((item) => (
            <li key={item._id}>
              {item.description} - {item.category}
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default ItemList;
