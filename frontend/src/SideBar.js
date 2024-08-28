import React from 'react';
import './SideBar.css';

function SideBar({ ads }) {
  return (
    <div className="sidebar">
      <h2>Sorted Ads</h2>
      <ul>
        {ads.map(ad => (
          <li key={ad.id}>
          {ad.name}
          <br />
          Reward : {ad.reward}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default SideBar;