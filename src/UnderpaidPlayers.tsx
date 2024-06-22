import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Player } from './types';
import PlayerModal from './PlayerModal';

const UnderpaidPlayers: React.FC = () => {
  const [underpaidPlayers, setUnderpaidPlayers] = useState<Player[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [modalPosition, setModalPosition] = useState({ top: 0, left: 0 });
  const listRef = useRef<HTMLUListElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/underpaid-players');
        setUnderpaidPlayers(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);

  const handleMouseEnter = (player: Player, event: React.MouseEvent<HTMLLIElement>) => {
    const listItem = event.currentTarget;
    const listRect = listRef.current?.getBoundingClientRect();
    const itemRect = listItem.getBoundingClientRect();
    if (listRect) {
      setModalPosition({
        top: itemRect.top - listRect.top,
        left: itemRect.right - listRect.left + 10,
      });
    }
    setSelectedPlayer(player);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-semibold mb-4">Most Underpaid Players</h2>
      <ul ref={listRef} className="space-y-2">
        {underpaidPlayers.map((player, index) => (
          <li
            key={index}
            className="p-3 bg-gray-100 rounded hover:bg-gray-200 transition-colors duration-200 cursor-pointer"
            onMouseEnter={(e) => handleMouseEnter(player, e)}
            onMouseLeave={() => setSelectedPlayer(null)}
          >
            <span className="font-medium">{player.name}</span>: ${player.salary.toLocaleString()} - Underpaid Metric: {player.overpaid_metric.toFixed(2)}
          </li>
        ))}
      </ul>
      {selectedPlayer && <PlayerModal player={selectedPlayer} position={modalPosition} />}
    </div>
  );
};

export default UnderpaidPlayers;