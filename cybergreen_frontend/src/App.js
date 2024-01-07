import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Chat from './Chat';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Top Banner */}
        <div className="banner">
          <img src="CyberGreen.jpg" alt="CyberGreen Banner" />
        </div>

        {/* Navigation Menu */}
        <nav className="menu">
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/evaluate">Evaluate</Link></li>
            <li><Link to="/leaderboard">Leaderboard</Link></li>
          </ul>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/evaluate" element={<ChatPage />} />
          {/* Add other routes as needed */}
        </Routes>

        {/* Center Aligned Button */}
        <div className="center-align">
          {/* Use Link to navigate to the 'evaluate' route */}
          <Link to="/evaluate">
            <button className="evaluate-button">Evaluate Your Ideas</button>
          </Link>
        </div>
      </div>
    </Router>
  );
}

function ChatPage() {
  return (
    <div>
      
      <Chat />
    </div>
  );
}

export default App;

