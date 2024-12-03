import React, { useState } from 'react';
import userService from '../services/userService'; 

const SellItem = () => {
  const [itemID, setItemID] = useState('');
  const [startingPrice, setStartingPrice] = useState('');
  const [startingTime, setStartingTime] = useState('');
  const [endingTime, setEndingTime] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const sellerID = localStorage.getItem('userId');
    if (!sellerID) {
      setMessage('You must be logged in to create an auction.');
      return;
    }

    const auctionData = {
      item_id: itemID,
      seller_id: sellerID,
      active: true,
      starting_time: startingTime,
      ending_time: endingTime,
      starting_price: parseFloat(startingPrice),
      current_price: parseFloat(startingPrice),
      bids: [],
    };

    try {
      await userService.createAuction(auctionData, sellerID); 
      setMessage('Auction created successfully!');
      setItemID('');
      setStartingPrice('');
      setStartingTime('');
      setEndingTime('');
    } catch (error) {
      console.error('Error creating auction:', error);
      setMessage('An error occurred while creating the auction.');
    }
  };

  return (
    <div>
      <h2>Create Auction</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Item ID:</label>
          <input
            type="text"
            value={itemID}
            onChange={(e) => setItemID(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Starting Price:</label>
          <input
            type="number"
            value={startingPrice}
            onChange={(e) => setStartingPrice(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Starting Time:</label>
          <input
            type="datetime-local"
            value={startingTime}
            onChange={(e) => setStartingTime(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Ending Time:</label>
          <input
            type="datetime-local"
            value={endingTime}
            onChange={(e) => setEndingTime(e.target.value)}
            required
          />
        </div>
        <button type="submit">Create Auction</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default SellItem;
