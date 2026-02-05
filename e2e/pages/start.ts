import { Page } from '@playwright/test';
import { HomePage } from './HomePage.js';

export class Start {
  constructor(private page: Page) {}

  async openHomePage(): Promise<HomePage> {
    const homePage = new HomePage(this.page);
    await homePage.open();
    return homePage;
  }

  async assumeHomePage(): Promise<HomePage> {
    const homePage = new HomePage(this.page);
    await homePage.assume();
    return homePage;
  }
}

export function start(page: Page): Start {
  return new Start(page);
}
