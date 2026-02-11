import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import TranscribeHome from './TranscribeHome.vue';
import UploadForm from '../components/UploadForm.vue';
import TranscriptResult from '../components/TranscriptResult.vue';

describe('TranscribeHome', () => {
  it('renders the main heading and description', () => {
    const wrapper = mount(TranscribeHome);

    expect(wrapper.find('h1').text()).toBe('Meeting Plunger');
    expect(wrapper.text()).toContain('Convert audio recordings to transcript');
  });

  it('renders UploadForm component', () => {
    const wrapper = mount(TranscribeHome);

    expect(wrapper.findComponent(UploadForm).exists()).toBe(true);
  });

  it('shows TranscriptResult when transcript is set', async () => {
    const wrapper = mount(TranscribeHome);

    // Initially, TranscriptResult should not be visible
    expect(wrapper.findComponent(TranscriptResult).exists()).toBe(false);

    // Emit transcript event from UploadForm
    const uploadForm = wrapper.findComponent(UploadForm);
    await uploadForm.vm.$emit('transcript', 'Hello, how are you?');

    // Now TranscriptResult should be visible
    expect(wrapper.findComponent(TranscriptResult).exists()).toBe(true);
  });
});

