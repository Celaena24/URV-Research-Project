import React, { useState, useEffect } from 'react';
import './App.css';

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

  const handleAdClick = (adId) => {
    fetch('http://127.0.0.1:5000/record_click', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ ad_id: adId }),
    }).catch(error => console.error('Error recording click:', error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Ad Rotator</h1>
      </header>
      <main>
        {isLoading ? (
          <div className="loading-message">Loading ads...</div>
        ) : (
          <div className="ad-slot">
            {displayedAds.map(ad => (
              <div key={ad.id} className="ad" onClick={() => handleAdClick(ad.id)}>
                {ad.content}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;