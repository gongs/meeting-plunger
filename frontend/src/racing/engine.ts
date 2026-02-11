export type Mode = 'normal' | 'super';

export const INITIAL_CONDITION = 6;

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

