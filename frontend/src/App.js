import React, { useState, useEffect } from 'react';
import './App.css';
import StarRating from './StarRating.js'

function App() {
  const [displayedAds, setDisplayedAds] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/ads')
      .then(response => response.json())
      .then(data => {
        setDisplayedAds(data);
        setIsLoading(false);
      })
      .catch(error => console.error('Error fetching ads:', error));
  }, []);


  return (
    <div className="App">
      <header className="App-header">
        <h1>Movie Recommendations</h1>
      </header>
      <main>
        {isLoading ? (
          <div className="loading-message">Loading ads...</div>
        ) : (
          <div className="ad-slot">
            {displayedAds.map(ad => (
              <div className = "ad">
                <div key={ad.id} className="ad-info">
                  {ad.content}
                </div>
                <StarRating adId={ad.id} />
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;