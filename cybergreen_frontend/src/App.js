// App.js

import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      {/* Top Banner */}
      <div className="banner">
        <img src="CyberGreen.jpg" alt="CyberGreen Banner" />
      </div>

      {/* Navigation Menu */}
      <nav className="menu">
        <ul>
          <li><a href="#">Home</a></li>
          <li><a href="#">Evaluate</a></li>
          <li><a href="#">Leaderboard</a></li>
        </ul>
      </nav>

      {/* Center Aligned Button */}
      <div className="center-align">
        <button className="evaluate-button">evaluate your idea</button>
      </div>
    </div>
  );
}

export default App;
