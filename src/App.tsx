import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

interface Player {
  name: string;
  salary: number;
  overpaid_metric: number;
}

function App() {
  const [overpaidPlayers, setOverpaidPlayers] = useState<Player[]>([]);
  const [highestPaidPlayers, setHighestPaidPlayers] = useState<Player[]>([]);
  const [underpaidPlayers, setUnderpaidPlayers] = useState<Player[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const overpaidResponse = await axios.get('http://127.0.0.1:5000/api/overpaid-players');
        setOverpaidPlayers(overpaidResponse.data);

        const highestPaidResponse = await axios.get('http://127.0.0.1:5000/api/highest-paid-players');
        setHighestPaidPlayers(highestPaidResponse.data);

        const underpaidResponse = await axios.get('http://127.0.0.1:5000/api/underpaid-players');
        setUnderpaidPlayers(underpaidResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <h1>NBA Player Statistics</h1>
      
      <h2>Most Overpaid Players</h2>
      <ul>
        {overpaidPlayers.map((player, index) => (
          <li key={index}>
            {player.name}: ${player.salary.toLocaleString()} - Overpaid Metric: {player.overpaid_metric.toFixed(2)}
          </li>
        ))}
      </ul>

      <h2>Highest Paid Players</h2>
      <ul>
        {highestPaidPlayers.map((player, index) => (
          <li key={index}>
            {player.name}: ${player.salary.toLocaleString()} - Overpaid Metric: {player.overpaid_metric.toFixed(2)}
          </li>
        ))}
      </ul>

      <h2>Most Underpaid Players</h2>
      <ul>
        {underpaidPlayers.map((player, index) => (
          <li key={index}>
            {player.name}: ${player.salary.toLocaleString()} - Underpaid Metric: {player.overpaid_metric.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;