export type { GameState, Mode, RollResult } from './types';
export { INITIAL_CONDITION, TRACK_LENGTH } from './types';

import type { GameState, Mode, RollResult } from './types';
import { INITIAL_CONDITION, TRACK_LENGTH } from './types';

export function advanceSteps(mode: Mode, dice: number, condition: number): number {
  if (mode === 'normal') {
    return dice % 2 === 0 ? 2 : 1;
  }
  return Math.min(dice, Math.max(0, condition));
}

export function hasWon(position: number): boolean {
  return position >= TRACK_LENGTH;
}

export function isGameOver(condition: number): boolean {
  return condition <= 0;
}

export function createInitialState(): GameState {
  return { position: 0, condition: INITIAL_CONDITION };
}

export function roll(state: GameState, mode: Mode, dice: number): RollResult {
  const steps = advanceSteps(mode, dice, state.condition);
  const newPosition = state.position + steps;
  const newCondition =
    mode === 'super' ? state.condition - 1 : state.condition;
  const won = hasWon(newPosition);
  const gameOver = !won && isGameOver(newCondition);

  return { steps, newPosition, newCondition, won, gameOver };
}

