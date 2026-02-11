export type Mode = 'normal' | 'super';

export const INITIAL_CONDITION = 6;
export const TRACK_LENGTH = 22;

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

