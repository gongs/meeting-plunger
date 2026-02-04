import { Given, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';

Given('I open the client application at {string}', async function (url) {
  await this.page.goto(url);
});

Then('the page title should contain {string}', async function (text) {
  const title = await this.page.title();
  expect(title).toContain(text);
});

Then('the page should display {string}', async function (text) {
  await expect(this.page.locator(`text=${text}`)).toBeVisible();
});
