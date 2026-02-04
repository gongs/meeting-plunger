import { Given, When, Then } from '@cucumber/cucumber';
import { expect } from '@playwright/test';

Given('the backend service is running on {string}', async function (url) {
  this.baseUrl = url;
});

Given('the client service is running on {string}', async function (url) {
  this.baseUrl = url;
});

When('I request the health endpoint', async function () {
  this.response = await this.page.request.get(`${this.baseUrl}/health`);
});

Then('the response status should be {int}', async function (statusCode) {
  expect(this.response.status()).toBe(statusCode);
});

Then('the response should contain {string}', async function (text) {
  const body = await this.response.json();
  const bodyString = JSON.stringify(body);
  expect(bodyString).toContain(text);
});
