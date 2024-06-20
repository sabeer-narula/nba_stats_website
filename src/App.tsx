import React from 'react';
import { BrowserRouter as Router, Route, Link, Routes } from 'react-router-dom';
import OverpaidPlayers from './OverpaidPlayers';
import HighestPaidPlayers from './HighestPaidPlayers';
import UnderpaidPlayers from './UnderpaidPlayers';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <h1>NBA Player Statistics</h1>
        <nav>
          <ul>
            <li>
              <Link to="/overpaid">Most Overpaid Players</Link>
            </li>
            <li>
              <Link to="/highest-paid">Highest Paid Players</Link>
            </li>
            <li>
              <Link to="/underpaid">Most Underpaid Players</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/overpaid" element={<OverpaidPlayers />} />
          <Route path="/highest-paid" element={<HighestPaidPlayers />} />
          <Route path="/underpaid" element={<UnderpaidPlayers />} />
          <Route path="/" element={<h2>Welcome to NBA Player Statistics</h2>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;