import { describe, it, expect } from 'vitest';
import {
  advanceSteps,
  applyDamage,
  createInitialState,
  hasWon,
  isGameOver,
  INITIAL_CONDITION,
  roll,
  TRACK_LENGTH,
} from './engine';

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

describe('end conditions', () => {
  it('uses a track length of 22 steps', () => {
    expect(TRACK_LENGTH).toBe(22);
  });

  it('wins when position is at or beyond the finish line', () => {
    expect(hasWon(21)).toBe(false);
    expect(hasWon(22)).toBe(true);
    expect(hasWon(23)).toBe(true);
  });

  it('ends the game when condition reaches 0', () => {
    expect(isGameOver(1)).toBe(false);
    expect(isGameOver(0)).toBe(true);
    expect(isGameOver(-1)).toBe(true);
  });
});

describe('roll', () => {
  it('creates an initial state', () => {
    expect(createInitialState()).toEqual({ position: 0, condition: 6 });
  });

  it('applies normal-mode steps and damage', () => {
    const result = roll(createInitialState(), 'normal', 1);
    expect(result).toEqual({
      steps: 1,
      newPosition: 1,
      newCondition: 5,
      won: false,
      gameOver: false,
    });
  });

  it('applies super-mode steps and damage', () => {
    const result = roll(createInitialState(), 'super', 6);
    expect(result.steps).toBe(6);
    expect(result.newPosition).toBe(6);
    expect(result.newCondition).toBe(6);
    expect(result.won).toBe(false);
    expect(result.gameOver).toBe(false);
  });

  it('wins when reaching or passing the finish line', () => {
    const result = roll({ position: 21, condition: 6 }, 'super', 2);
    expect(result.won).toBe(true);
    expect(result.gameOver).toBe(false);
  });

  it('ends the game when condition reaches 0 before winning', () => {
    const result = roll({ position: 0, condition: 1 }, 'normal', 1);
    expect(result.won).toBe(false);
    expect(result.gameOver).toBe(true);
  });

  it('treats reaching the finish line as a win even if condition drops to 0', () => {
    const result = roll({ position: 21, condition: 1 }, 'super', 1);
    expect(result.won).toBe(true);
    expect(result.gameOver).toBe(false);
  });
});

