import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';
import path from 'path';

Given(
  'OpenAI transcription API replys the following when the model is {string}:',
  async function (model, docString) {
    // TODO: Mock OpenAI API - skip for now
  }
);

When('I convert the audio file {string} into text', async function (filename) {
  // Navigate to the client application
  await this.page.goto('http://localhost:3000');

  // Find the file upload control (with shorter timeout for clearer error)
  const fileInput = this.page.locator('input[type="file"]');
  await fileInput.waitFor({ timeout: 3000 });

  // Upload the fixture file
  const fixturePath = path.join(process.cwd(), 'fixtures', filename);
  await fileInput.setInputFiles(fixturePath);

  // Click the upload button
  const uploadButton = this.page.locator('button:has-text("Upload")');
  await uploadButton.click();
});

Then('the text should be {string}', async function (expectedText) {
  // Wait for and verify the transcription result
  const result = this.page.locator('text=' + expectedText);
  await expect(result).toBeVisible();
});
