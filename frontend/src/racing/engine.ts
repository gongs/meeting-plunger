export type Mode = 'normal' | 'super';

export function advanceSteps(mode: Mode, dice: number): number {
  if (mode === 'normal') {
    return dice % 2 === 0 ? 2 : 1;
  }

  return dice;
}

