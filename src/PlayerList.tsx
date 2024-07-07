import React, { useState, useCallback } from 'react';
import InfiniteScroll from 'react-infinite-scroll-component';
import { Player } from './types';
import PlayerModal from './PlayerModal';

interface PlayerListProps {
  players: Player[];
  title: string;
  isUnderpaid: boolean;
}

const PlayerList: React.FC<PlayerListProps> = ({ players, title, isUnderpaid }) => {
  const [selectedPlayer, setSelectedPlayer] = useState<Player | null>(null);
  const [modalPosition, setModalPosition] = useState({ top: 0, left: 0 });
  const [searchTerm, setSearchTerm] = useState('');
  const [displayedPlayers, setDisplayedPlayers] = useState<Player[]>(players.slice(0, 20));

  const handleMouseEnter = (player: Player, event: React.MouseEvent<HTMLLIElement>) => {
    const rect = event.currentTarget.getBoundingClientRect();
    setModalPosition({
      top: rect.top + window.scrollY,
      left: rect.right + 10, // 10px to the right of the list item
    });
    setSelectedPlayer(player);
  };

  const filteredPlayers = players.filter(player =>
    player.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const fetchMoreData = () => {
    const currentLength = displayedPlayers.length;
    const more = filteredPlayers.slice(currentLength, currentLength + 20);
    setDisplayedPlayers([...displayedPlayers, ...more]);
  };

  const handleSearch = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
    setDisplayedPlayers(filteredPlayers.slice(0, 20));
  }, [filteredPlayers]);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-semibold mb-4">{title}</h2>
      <input
        type="text"
        placeholder="Search players..."
        value={searchTerm}
        onChange={handleSearch}
        className="w-full p-2 mb-4 border rounded"
      />
      <div id="scrollableDiv" style={{ height: '600px', overflow: 'auto' }}>
        <InfiniteScroll
          dataLength={displayedPlayers.length}
          next={fetchMoreData}
          hasMore={displayedPlayers.length < filteredPlayers.length}
          loader={<h4>Loading...</h4>}
          scrollableTarget="scrollableDiv"
        >
          <ul className="space-y-2">
            {displayedPlayers.map((player, index) => (
              <li
                key={index}
                className="p-3 bg-gray-100 rounded hover:bg-gray-200 transition-colors duration-200 cursor-pointer"
                onMouseEnter={(e) => handleMouseEnter(player, e)}
                onMouseLeave={() => setSelectedPlayer(null)}
              >
                <span className="font-medium">{index + 1}. {player.name}</span>: ${player.salary.toLocaleString()} - 
                {isUnderpaid ? 'Underpaid' : 'Overpaid'} Metric: {player.overpaid_metric.toFixed(2)}
              </li>
            ))}
          </ul>
        </InfiniteScroll>
      </div>
      {selectedPlayer && (
        <PlayerModal
          player={selectedPlayer}
          position={modalPosition}
          isUnderpaid={isUnderpaid}
        />
      )}
    </div>
  );
};

export default PlayerList;