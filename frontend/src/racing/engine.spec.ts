import { describe, it, expect } from 'vitest';
import {
  advanceSteps,
  createInitialState,
  hasWon,
  isGameOver,
  INITIAL_CONDITION,
  roll,
  TRACK_LENGTH,
} from './engine';

describe('advanceSteps', () => {
  it('moves 1 step on odd dice in normal mode', () => {
    expect(advanceSteps('normal', 1, 6)).toBe(1);
    expect(advanceSteps('normal', 3, 6)).toBe(1);
    expect(advanceSteps('normal', 5, 6)).toBe(1);
  });

  it('moves 2 steps on even dice in normal mode', () => {
    expect(advanceSteps('normal', 2, 6)).toBe(2);
    expect(advanceSteps('normal', 4, 6)).toBe(2);
    expect(advanceSteps('normal', 6, 6)).toBe(2);
  });

  it('moves min(dice, condition) steps in super mode', () => {
    expect(advanceSteps('super', 1, 6)).toBe(1);
    expect(advanceSteps('super', 2, 6)).toBe(2);
    expect(advanceSteps('super', 6, 6)).toBe(6);
    expect(advanceSteps('super', 6, 3)).toBe(3);
    expect(advanceSteps('super', 5, 2)).toBe(2);
  });

  it('returns 0 steps in super mode when condition is 0', () => {
    expect(advanceSteps('super', 6, 0)).toBe(0);
  });
});

describe('INITIAL_CONDITION', () => {
  it('starts with 6 condition points', () => {
    expect(INITIAL_CONDITION).toBe(6);
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

  it('applies normal-mode steps and no condition damage', () => {
    const result = roll(createInitialState(), 'normal', 1);
    expect(result).toEqual({
      steps: 1,
      newPosition: 1,
      newCondition: 6,
      won: false,
      gameOver: false,
    });
  });

  it('applies super-mode steps and 1 condition damage per roll', () => {
    const result = roll(createInitialState(), 'super', 6);
    expect(result.steps).toBe(6);
    expect(result.newPosition).toBe(6);
    expect(result.newCondition).toBe(5);
    expect(result.won).toBe(false);
    expect(result.gameOver).toBe(false);
  });

  it('caps super-mode steps by condition when dice > condition', () => {
    const result = roll({ position: 0, condition: 3 }, 'super', 6);
    expect(result.steps).toBe(3);
    expect(result.newPosition).toBe(3);
    expect(result.newCondition).toBe(2);
  });

  it('wins when reaching or passing the finish line', () => {
    const result = roll({ position: 21, condition: 6 }, 'super', 2);
    expect(result.won).toBe(true);
    expect(result.gameOver).toBe(false);
  });

  it('ends the game when condition reaches 0 before winning in super mode', () => {
    const result = roll({ position: 0, condition: 1 }, 'super', 1);
    expect(result.won).toBe(false);
    expect(result.gameOver).toBe(true);
    expect(result.newCondition).toBe(0);
  });

  it('treats reaching the finish line as a win even if condition drops to 0', () => {
    const result = roll({ position: 21, condition: 1 }, 'super', 1);
    expect(result.won).toBe(true);
    expect(result.gameOver).toBe(false);
  });
});

