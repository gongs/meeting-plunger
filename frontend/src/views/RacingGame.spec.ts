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
});

