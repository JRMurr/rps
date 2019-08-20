import { Box, makeStyles, Typography } from '@material-ui/core';
import classNames from 'classnames';
import React, { useContext } from 'react';
import { LiveMatchContext } from 'state/livematch';
import { GameOutcome } from 'state/match';
import { countGameOutcomes } from 'util/funcs';
import { Check as CheckIcon } from '@material-ui/icons';

const useLocalStyles = makeStyles(({ spacing }) => ({
  root: {
    // Use a fixed width here so that the game log will be exactly centered
    width: 120,
  },
  rtl: {
    // Need this so we overflow to the left
    direction: 'rtl',
  },
  statusIcon: {
    margin: `0 ${spacing(0.5)}px`,
  },
}));

interface Props {
  className?: string;
  isSelf: boolean;
}

// We have to leave the React.FC tag off to get default props to work
const PlayerScore: React.FC<Props> & { defaultProps: Partial<Props> } = ({
  className,
  isSelf,
}) => {
  const localClasses = useLocalStyles();
  const {
    state: {
      data: { games, opponent },
    },
  } = useContext(LiveMatchContext);

  const num = countGameOutcomes(
    games,
    isSelf ? GameOutcome.Win : GameOutcome.Loss
  );
  const name = isSelf ? 'You' : opponent ? opponent.name : 'No Opponent';
  const showReadyIcon = !isSelf && opponent && opponent.isReady;

  return (
    <div
      className={classNames(localClasses.root, className, {
        [localClasses.rtl]: !isSelf,
      })}
    >
      <Box display="flex" flexDirection="row" alignItems="center">
        <Typography variant="h5" noWrap>
          {name}
        </Typography>
        {showReadyIcon && <CheckIcon className={localClasses.statusIcon} />}
      </Box>
      <Typography variant="h4">{num}</Typography>
    </div>
  );
};

PlayerScore.defaultProps = {
  isSelf: false,
};

export default PlayerScore;
