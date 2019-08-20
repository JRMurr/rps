import { ConnectionStatus } from 'hooks/useWebSocket';
import { sample } from 'lodash';
import { useEffect, useState } from 'react';
import { MatchOutcome } from 'state/match';
import useUser from './useUser';

type Key = string | number | symbol;
type Splashes<T extends Key = string> = Record<T, string[]>;
type Splasher<T = string> = (key: T, isAlt: boolean) => string;

const welcomeSplashes: Splashes = {
  '': [
    'Welcome!',
    'Bienvenidos!',
    'Tere tulemast!',
    'Wilkommen!',
    'пожалуйста',
    '欢迎',
  ],
};

const connectionStatusSplashes: Splashes<ConnectionStatus> = {
  [ConnectionStatus.Connecting]: [`Oooooh, he's trying!`],
  [ConnectionStatus.Connected]: [
    'You are Online™',
    'Welcome to the THUNDERDOME',
  ],
  [ConnectionStatus.ClosedError]: [':sad_parrot:'],
  [ConnectionStatus.ClosedNormal]: ['Head aega!', 'Nägemist!', 'Nägemiseni!'],
};

const matchOutcomeSplashes: Splashes<MatchOutcome> = {
  [MatchOutcome.Win]: ['gg ez', 'gg no re', 'ez game ez life'],
  [MatchOutcome.Loss]: [
    'Damn, you just got dumpstered',
    'Embarrassing',
    'You are a disgrace to your family',
    "You friggin'  moron, you just got porched",
  ],
};

const makeSplasher = <T extends Key>(
  splashes: Splashes<T>,
  altSplashes?: Splashes<T>
): Splasher<T> => {
  return (key, isAlt) => {
    const toSample = isAlt && altSplashes ? altSplashes : splashes;
    return sample(toSample[key]) || '';
  };
};

export const welcomeSplasher: Splasher = makeSplasher(welcomeSplashes);

export const connectionStatusSplasher: Splasher<
  ConnectionStatus
> = makeSplasher(connectionStatusSplashes);

export const matchOutcomeSplasher: Splasher<MatchOutcome> = makeSplasher(
  matchOutcomeSplashes
);

/**
 * EXTREMELY important hook. Integral to the operation of the entire program.
 */
const useSplashMessage = <T extends Key>(
  splasher: Splasher<T>,
  key?: T
): string => {
  const user = useUser();
  const isAlt = Boolean(user && user.username.toLowerCase() === 'nick'); // lol

  const [splash, setSplash] = useState('');
  useEffect(() => setSplash(key !== undefined ? splasher(key, isAlt) : ''), [
    splasher,
    key,
    isAlt,
  ]);
  return splash;
};

export default useSplashMessage;
