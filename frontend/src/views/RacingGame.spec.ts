import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import RacingGame from './RacingGame.vue';

describe('RacingGame', () => {
  it('rolls the dice and shows dice/steps/position', async () => {
    const wrapper = mount(RacingGame, {
      props: {
        diceRoller: () => 2,
      },
    });

    expect(wrapper.get('[data-testid="position"]').text()).toContain('0');

    await wrapper.get('[data-testid="roll"]').trigger('click');

    expect(wrapper.get('[data-testid="dice"]').text()).toContain('2');
    expect(wrapper.get('[data-testid="steps"]').text()).toContain('2');
    expect(wrapper.get('[data-testid="position"]').text()).toContain('2');
  });

  it('uses super mode when selected', async () => {
    const wrapper = mount(RacingGame, {
      props: {
        diceRoller: () => 3,
      },
    });

    await wrapper.get('[data-testid="mode-super"]').trigger('click');
    await wrapper.get('[data-testid="roll"]').trigger('click');

    expect(wrapper.get('[data-testid="dice"]').text()).toContain('3');
    expect(wrapper.get('[data-testid="steps"]').text()).toContain('3');
    expect(wrapper.get('[data-testid="position"]').text()).toContain('3');
  });

  it('shows condition and decreases it when dice is 1', async () => {
    const wrapper = mount(RacingGame, {
      props: {
        diceRoller: () => 1,
      },
    });

    expect(wrapper.get('[data-testid="condition"]').text()).toContain('6');

    await wrapper.get('[data-testid="roll"]').trigger('click');

    expect(wrapper.get('[data-testid="condition"]').text()).toContain('5');
    expect(wrapper.get('[data-testid="damage"]').text()).toContain('Damage +1');
  });
});

