import camelcaseKeys from 'camelcase-keys';
import withRouteParams from 'hoc/withRouteParams';
import useWebSocket, { ConnectionStatus } from 'hooks/useWebSocket';
import React, { useReducer, useCallback } from 'react';
import {
  LiveMatchActionType,
  LiveMatchContext,
  liveMatchReducer,
  LiveMatchData,
  LiveMatchError,
  defaultLiveMatchState,
} from 'state/livematch';
import ConnectionIndicator from './ConnectionIndicator';
import LiveMatch from './LiveMatch';
import { Typography, LinearProgress } from '@material-ui/core';

interface Props {
  matchId: string;
}

/**
 * Data handler for the match screen.
 */
const LiveMatchView: React.FC<Props> = ({ matchId }) => {
  const [state, dispatch] = useReducer(liveMatchReducer, defaultLiveMatchState);
  const { status, send } = useWebSocket(
    `/ws/match/${matchId}`,
    // We need to memoize the callbacks to prevent hook triggers
    // Ugly solution but it works (sorry Seth!)
    {
      onMessage: useCallback(data => {
        if (data.error) {
          dispatch({
            type: LiveMatchActionType.Error,
            error: (data as unknown) as LiveMatchError,
          });
        } else {
          // Let's just pray our data format agrees with the API
          dispatch({
            type: LiveMatchActionType.MatchUpdate,
            data: (camelcaseKeys(data, {
              deep: true,
            }) as unknown) as LiveMatchData,
          });
        }
      }, []),
    }
  );

  if (status === ConnectionStatus.Connecting) {
    return (
      <>
        <Typography>Connecting to server...</Typography>
        <LinearProgress />
      </>
    );
  }

  return (
    <LiveMatchContext.Provider
      value={{
        connectionStatus: status,
        sendMessage: send,
        state,
      }}
    >
      <LiveMatch />
      <ConnectionIndicator />
    </LiveMatchContext.Provider>
  );
};

export default withRouteParams(LiveMatchView);
