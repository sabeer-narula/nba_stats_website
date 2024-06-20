import React from 'react';
import { Player } from './types';

interface PlayerModalProps {
  player: Player;
  position: { top: number; left: number };
}

const PlayerModal: React.FC<PlayerModalProps> = ({ player, position }) => {
  const stats = Object.entries(player).filter(([key, _]) => 
    !['name', 'salary', 'overpaid_metric'].includes(key)
  );

  return (
    <div className="modal" style={{ top: `${position.top}px`, left: `${position.left}px` }}>
      <h3>{player.name}</h3>
      <p>Salary: ${player.salary.toLocaleString()}</p>
      {stats.map(([key, value]) => (
        <p key={key}>{key}: {typeof value === 'number' ? value.toFixed(3) : value}</p>
      ))}
    </div>
  );
};

export default PlayerModal;