import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Chat from './Chat';
import CsvFileUploader from './Upload';
import './App.css';
import Leaderboard from './Leaderboard';

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
            <li><Link to="/evaluate">Evaluate</Link></li>
            <li><Link to="/leaderboard">Leaderboard</Link></li>
          </ul>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/evaluate/*" element={<EvaluatePage />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/" element={<EvaluatePage />} />
          {/* Add other routes as needed */}
        </Routes>
      </div>
    </Router>
  );
}

function EvaluatePage() {
  return (
    <div className="evaluate-page">
      <Chat className="Chat"/>
      <CsvFileUploader className="Upload"/>
    </div>
  );
}

export default App;

