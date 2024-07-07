import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Player } from './types';
import PlayerList from './PlayerList';

function App() {
  const [overpaidPlayers, setOverpaidPlayers] = useState<Player[]>([]);
  const [highestPaidPlayers, setHighestPaidPlayers] = useState<Player[]>([]);
  const [underpaidPlayers, setUnderpaidPlayers] = useState<Player[]>([]);
  const [activeView, setActiveView] = useState<'overpaid' | 'highestPaid' | 'underpaid'>('overpaid');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const [overpaidResponse, highestPaidResponse, underpaidResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/api/overpaid-players'),
          axios.get('http://127.0.0.1:5000/api/highest-paid-players'),
          axios.get('http://127.0.0.1:5000/api/underpaid-players')
        ]);

        setOverpaidPlayers(overpaidResponse.data);
        setHighestPaidPlayers(highestPaidResponse.data);
        setUnderpaidPlayers(underpaidResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Failed to fetch player data. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <div className="text-center mt-8">Loading...</div>;
  }

  if (error) {
    return <div className="text-center mt-8 text-red-600">{error}</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <header className="bg-blue-600 text-white shadow-lg">
        <div className="container mx-auto py-4 px-6">
          <h1 className="text-3xl font-bold">NBA Player Statistics</h1>
        </div>
      </header>
      <main className="container mx-auto mt-8 px-6">
        <div className="mb-6">
          <button
            className={`mr-4 px-4 py-2 rounded ${activeView === 'overpaid' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveView('overpaid')}
          >
            Overpaid Players
          </button>
          <button
            className={`mr-4 px-4 py-2 rounded ${activeView === 'highestPaid' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveView('highestPaid')}
          >
            Highest Paid Players
          </button>
          <button
            className={`px-4 py-2 rounded ${activeView === 'underpaid' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
            onClick={() => setActiveView('underpaid')}
          >
            Underpaid Players
          </button>
        </div>
        {activeView === 'overpaid' && (
          <PlayerList players={overpaidPlayers} title="Top 100 Most Overpaid Players" isUnderpaid={false} />
        )}
        {activeView === 'highestPaid' && (
          <PlayerList players={highestPaidPlayers} title="Highest Paid Players" isUnderpaid={false} />
        )}
        {activeView === 'underpaid' && (
          <PlayerList players={underpaidPlayers} title="Top 100 Most Underpaid Players" isUnderpaid={true} />
        )}
      </main>
    </div>
  );
}

export default App;