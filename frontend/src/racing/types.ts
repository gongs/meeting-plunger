export type Mode = 'normal' | 'super';

export type GameState = {
  position: number;
  condition: number;
};

export type RollResult = {
  steps: number;
  newPosition: number;
  newCondition: number;
  won: boolean;
  gameOver: boolean;
};

export const INITIAL_CONDITION = 6;
export const TRACK_LENGTH = 22;

