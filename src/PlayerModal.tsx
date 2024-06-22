import React from 'react';
import { Player } from './types';

interface PlayerModalProps {
  player: Player;
  position: { top: number; left: number };
}

const PlayerModal: React.FC<PlayerModalProps> = ({ player, position }) => {
  const getSpecificPlayerMessage = (player: Player): string | null => {
    const specificMessages: { [key: string]: string } = {
      "Klay Thompson": `gets paid $${player.salary.toLocaleString()} to go 0/10 in an elimination game`,
      "Jordan Poole": `gets paid $${player.salary.toLocaleString()} to have a -7.1 plus minus and stare at baddies on the sideline`,
      "Stephen Curry": `gets paid $${player.salary.toLocaleString()}...`,
      "Nikola Jokic": `gets paid $${player.salary.toLocaleString()} to daydream about horses in Serbia all game`,
      "LeBron James": `gets paid $${player.salary.toLocaleString()} to practice nepotism`,
      "Zion Williamson": `gets paid $${player.salary.toLocaleString()} to start a food blogging channel`,
      "Ja Morant": `gets paid $${player.salary.toLocaleString()} to practice his sharpshooting on the sidelines`,
    };

    return specificMessages[player.name] || null;
  }

  const getStatDescription = (stat: string, value: number): string => {
    switch (stat) {
      case 'FG3_PCT':
        return `shoot ${(value * 100).toFixed(1)}% from 3`;
      case 'GP':
        return `play ${value} games this season`;
      case 'PTS':
        return `put up ${value.toFixed(1)} points per game`;
      case 'TOV':
        return `turn the ball over ${value.toFixed(1)} times per game`;
      case 'PLUS_MINUS':
        return `have a ${value.toFixed(1)} plus minus`;
      case 'FT_PCT':
        return `shoot free throws at ${(value * 100).toFixed(1)}%`;
      case 'AST':
        return `dish out ${value.toFixed(1)} assists per game`;
      case 'BLK':
        return `block ${value.toFixed(1)} shots per game`;
      case 'OREB':
        return `grab ${value.toFixed(1)} offensive rebounds per game`;
      case 'DREB':
        return `secure ${value.toFixed(1)} defensive rebounds per game`;
      default:
        return `${stat.toLowerCase().replace('_', ' ')}: ${value.toFixed(1)}`;
    }
  };

  const specificMessage = getSpecificPlayerMessage(player);

  if (specificMessage) {
    return (
      <div className="absolute bg-blue-600 text-white p-4 rounded-lg shadow-lg z-50 max-w-xs" style={{ top: `${position.top}px`, left: `${position.left}px` }}>
        <p className="text-sm">{player.name} {specificMessage}.</p>
      </div>
    );
  }

  const worstStatsArray = Object.entries(player.worst_stats)
    .map(([stat, value]) => getStatDescription(stat, value));

  const worstStatsDescription = worstStatsArray.length > 1
    ? worstStatsArray.slice(0, -1).join(', ') + ', and ' + worstStatsArray.slice(-1)
    : worstStatsArray[0];

  return (
    <div className="absolute bg-blue-600 text-white p-4 rounded-lg shadow-lg z-50 max-w-xs" style={{ top: `${position.top}px`, left: `${position.left}px` }}>
      <p className="text-sm">{player.name} gets paid ${player.salary.toLocaleString()} to {worstStatsDescription}.</p>
    </div>
  );
};

export default PlayerModal;










// const PlayerModal: React.FC<PlayerModalProps> = ({ player, position }) => {
//     const getSpecificPlayerMessage = (player: Player): string | null => {
//       const specificMessages: { [key: string]: string } = {
//         "Klay Thompson": `gets paid $${player.salary.toLocaleString()} to go 0/10 in an elimination game`,
//         "Jordan Poole": `gets paid $${player.salary.toLocaleString()} to have a -7.1 plus minus and stare at baddies on the sideline`,
//         "Stephen Curry": `gets paid $${player.salary.toLocaleString()}...`,
//         "Nikola Jokic": `gets paid $${player.salary.toLocaleString()} to daydream about horses in Serbia all game`,
//         "LeBron James": `gets paid $${player.salary.toLocaleString()} to practice nepotism`,
//         "Zion Williamson": `gets paid $${player.salary.toLocaleString()} to start a food blogging channel`,
//         "Ja Morant": `gets paid $${player.salary.toLocaleString()} to practice his sharpshooting on the sidelines`,
//       };