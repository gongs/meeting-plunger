import { describe, it, expect } from 'vitest';
import { advanceSteps, applyDamage, INITIAL_CONDITION } from './engine';

describe('advanceSteps', () => {
  it('moves 1 step on odd dice in normal mode', () => {
    expect(advanceSteps('normal', 1)).toBe(1);
    expect(advanceSteps('normal', 3)).toBe(1);
    expect(advanceSteps('normal', 5)).toBe(1);
  });

  it('moves 2 steps on even dice in normal mode', () => {
    expect(advanceSteps('normal', 2)).toBe(2);
    expect(advanceSteps('normal', 4)).toBe(2);
    expect(advanceSteps('normal', 6)).toBe(2);
  });

  it('moves N steps on dice value in super mode', () => {
    expect(advanceSteps('super', 1)).toBe(1);
    expect(advanceSteps('super', 2)).toBe(2);
    expect(advanceSteps('super', 6)).toBe(6);
  });
});

describe('applyDamage', () => {
  it('starts with 6 condition points', () => {
    expect(INITIAL_CONDITION).toBe(6);
  });

  it('decreases condition by 1 when dice is 1', () => {
    expect(applyDamage(6, 1)).toBe(5);
  });

  it('does not change condition when dice is not 1', () => {
    expect(applyDamage(6, 2)).toBe(6);
    expect(applyDamage(6, 6)).toBe(6);
  });
});

