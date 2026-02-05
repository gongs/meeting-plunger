import { Given, When, Then } from '@cucumber/cucumber';
import { CustomWorld } from '../support/world.js';
import { start } from '../pages/start.js';

Given(
  'OpenAI transcription API replys the following when the model is {string}:',
  async function (this: CustomWorld, _model: string, _docString: string) {
    // TODO: Mock OpenAI API - skip for now
  }
);

When(
  'I convert the audio file {string} into transcript',
  async function (this: CustomWorld, filename: string) {
    if (!this.page) throw new Error('Page is not initialized');

    const homePage = await start(this.page).openHomePage();
    await homePage.uploadAudioFile(filename);
  }
);

Then(
  'the transcript should be {string}',
  async function (this: CustomWorld, expectedTranscript: string) {
    if (!this.page) throw new Error('Page is not initialized');

    const homePage = await start(this.page).assumeHomePage();
    await homePage.verifyTranscript(expectedTranscript);
  }
);
