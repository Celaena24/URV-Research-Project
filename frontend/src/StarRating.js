
import React, { useState } from 'react';
import axios from 'axios';
import ReactStars from 'react-rating-stars-component';
import "./StarRating.css"

const StarRating = ({ adId }) => {
  const [rating, setRating] = useState(null);

  const ratingChanged = (newRating) => {
    setRating(newRating);
    axios.post('http://localhost:5000/submit-rating', { id: adId, rating: newRating })
      .then(response => {
        console.log(response.data);
        alert('Rating submitted successfully!');
      })
      .catch(error => {
        console.error('Error submitting rating:', error);
      });
  };

  return (
    <div className="star-rating-container">
      <ReactStars
        count={5}
        onChange={ratingChanged}
        size={30}
        activeColor="#ffd700"
      />
    </div>
  );
};

export default StarRating;
