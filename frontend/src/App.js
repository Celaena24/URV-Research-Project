import React, { useState, useEffect } from 'react';
import './App.css';
import SideBar from './SideBar.js';

function App() {
  const [displayedAds, setDisplayedAds] = useState([]);
  const [sortedAds, setSortedAds] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:5000/all_ads')
      .then(response => response.json())
      .then(data => {
        setSortedAds(data); // Sort ads by rating
      })
      .catch(error => console.error('Error fetching ads:', error));
  }, []);
  useEffect(() => {
    fetch('http://127.0.0.1:5000/ads')
      .then(response => response.json())
      .then(data => {
        setDisplayedAds(data);
        setIsLoading(false);
      })
      .catch(error => console.error('Error fetching ads:', error));
  }, []);

  console.log(displayedAds)
  return (
    <div className="App">
      <header className="App-header">
        <h1>Movie Recommendations</h1>
      </header>
      <main>
        <SideBar ads={sortedAds} />
        {isLoading ? (
          <div className="loading-message">Loading ads...</div>
        ) : (
          <div>
            <h2>Top 3 ads using ETC Algorithm</h2>
            <div className="ad-slot">
              {displayedAds.map(ad => (
                <div key={ad.id} className="ad">
                  <div className="ad-info">
                    <p>{ad.name}</p>
                    <p>Genre: {ad.genre}</p>
                    <p>Age-restriction: {ad.age_restriction}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;