import { CircularProgress } from '@material-ui/core';
import React from 'react';
import { Move } from 'state/match';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { IconName } from '@fortawesome/fontawesome-svg-core';

/**
 * Mapping of move->icon. We need this in an object to convince TS that the
 * icons names are always valid.
 */
const moveIcons: { [move: string]: IconName } = {
  [Move.Rock]: 'hand-rock',
  [Move.Paper]: 'hand-paper',
  [Move.Scissors]: 'hand-scissors',
  [Move.Lizard]: 'hand-lizard',
  [Move.Spock]: 'hand-spock',
};

/**
 * An icon for a single move. If no move is specified, a loading icon is shown
 */
const MoveIcon: React.FC<{
  move?: Move;
}> = ({ move }) =>
  move ? (
    <FontAwesomeIcon icon={moveIcons[move]} />
  ) : (
    // <Typography>{moveLabels[move]}</Typography>
    <CircularProgress size={20} />
  );

export default MoveIcon;
