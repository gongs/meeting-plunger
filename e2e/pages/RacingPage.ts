import { Page, expect } from '@playwright/test';

export class RacingPage {
  constructor(private page: Page) {}

  async open(): Promise<this> {
    await this.page.goto('http://localhost:3000/racing');
    return this;
  }

  async assume(): Promise<this> {
    const heading = this.page.locator('h1:has-text("Racing Game")');
    await expect(heading).toBeVisible({ timeout: 3000 });
    return this;
  }

  async selectSuperMode(): Promise<this> {
    await this.page.locator('[data-testid="mode-super"]').click();
    return this;
  }

  async rollOnce(): Promise<this> {
    await this.page.locator('[data-testid="roll"]').click();
    return this;
  }

  async getDisplayedDice(): Promise<number> {
    const text = await this.page.locator('[data-testid="dice"]').innerText();
    return Number.parseInt(text.trim(), 10);
  }

  async getDisplayedSteps(): Promise<number> {
    const text = await this.page.locator('[data-testid="steps"]').innerText();
    return Number.parseInt(text.trim(), 10);
  }
}

