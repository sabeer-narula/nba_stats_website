import React from 'react';
import { Player } from './types';

interface PlayerModalProps {
  player: Player;
  position: { top: number; left: number };
}

const PlayerModal: React.FC<PlayerModalProps> = ({ player, position }) => {
  return (
    <div className="modal" style={{ top: `${position.top}px`, left: `${position.left}px` }}>
      <h3>{player.name}</h3>
      <p>Salary: ${player.salary.toLocaleString()}</p>
      <p>Overpaid Metric: {player.overpaid_metric.toFixed(2)}</p>
      
      <h4>Best Stats:</h4>
      <ul>
        {Object.entries(player.best_stats).map(([stat, value]) => (
          <li key={stat}>{stat}: {typeof value === 'number' ? value.toFixed(1) : value}</li>
        ))}
      </ul>
      
      <h4>Worst Stats:</h4>
      <ul>
        {Object.entries(player.worst_stats).map(([stat, value]) => (
          <li key={stat}>{stat}: {typeof value === 'number' ? value.toFixed(1) : value}</li>
        ))}
      </ul>
    </div>
  );
};

export default PlayerModal;