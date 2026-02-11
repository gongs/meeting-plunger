import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import App from './App.vue';

describe('App', () => {
  it('renders the top navigation', () => {
    const wrapper = mount(App, {
      global: {
        stubs: {
          RouterLink: { template: '<a><slot /></a>' },
          RouterView: { template: '<div />' },
        },
      },
    });

    expect(wrapper.text()).toContain('Meeting Plunger');
    expect(wrapper.text()).toContain('Transcribe');
    expect(wrapper.text()).toContain('Racing');
  });
});
