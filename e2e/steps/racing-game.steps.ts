import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import { CustomWorld } from '../support/world.js';
import { start } from '../pages/start.js';

Given('I open the racing game', async function (this: CustomWorld) {
  if (!this.page) throw new Error('Page is not initialized');

  const racingPage = await start(this.page).openRacingPage();
  await racingPage.assume();
});

When(
  'I select super mode and roll once',
  async function (this: CustomWorld) {
    if (!this.page) throw new Error('Page is not initialized');

    const racingPage = await start(this.page).assumeRacingPage();
    await racingPage.selectSuperMode();
    await racingPage.rollOnce();
  }
);

Then(
  'the displayed steps should equal the displayed dice',
  async function (this: CustomWorld) {
    if (!this.page) throw new Error('Page is not initialized');

    const racingPage = await start(this.page).assumeRacingPage();
    const dice = await racingPage.getDisplayedDice();
    const steps = await racingPage.getDisplayedSteps();

    expect(steps).toBe(dice);
  }
);

