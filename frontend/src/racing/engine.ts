export type Mode = 'normal' | 'super';

export const INITIAL_CONDITION = 6;
export const TRACK_LENGTH = 22;

export type GameState = {
  position: number;
  condition: number;
};

export function advanceSteps(mode: Mode, dice: number): number {
  if (mode === 'normal') {
    return dice % 2 === 0 ? 2 : 1;
  }

  return dice;
}

export function applyDamage(condition: number, dice: number): number {
  if (dice === 1) return condition - 1;
  return condition;
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

export type RollResult = {
  steps: number;
  newPosition: number;
  newCondition: number;
  won: boolean;
  gameOver: boolean;
};

export function roll(state: GameState, mode: Mode, dice: number): RollResult {
  const steps = advanceSteps(mode, dice);
  const newPosition = state.position + steps;
  const newCondition = applyDamage(state.condition, dice);
  const won = hasWon(newPosition);
  const gameOver = !won && isGameOver(newCondition);

  return { steps, newPosition, newCondition, won, gameOver };
}

