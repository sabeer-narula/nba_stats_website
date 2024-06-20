import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Player } from './types';
import PlayerModal from './PlayerModal';

const OverpaidPlayers: React.FC = () => {
  const [overpaidPlayers, setOverpaidPlayers] = useState<Player[]>([]);
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [modalPosition, setModalPosition] = useState({ top: 0, left: 0 });
  const listRef = useRef<HTMLUListElement>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/overpaid-players');
        setOverpaidPlayers(response.data);
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
        left: itemRect.right - listRect.left + 10, // 10px offset from the list item
      });
    }

    setSelectedPlayer(player);
  };

  return (
    <div className="player-list-container">
      <h2>Most Overpaid Players</h2>
      <ul ref={listRef}>
        {overpaidPlayers.map((player, index) => (
          <li
            key={index}
            onMouseEnter={(e) => handleMouseEnter(player, e)}
            onMouseLeave={() => setSelectedPlayer(null)}
          >
            {player.name}: ${player.salary.toLocaleString()} - Overpaid Metric: {player.overpaid_metric.toFixed(2)}
          </li>
        ))}
      </ul>
      {selectedPlayer && <PlayerModal player={selectedPlayer} position={modalPosition} />}
    </div>
  );
};

export default OverpaidPlayers;