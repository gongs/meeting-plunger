import { Page } from '@playwright/test';
import { HomePage } from './HomePage.js';
import { RacingPage } from './RacingPage.js';

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

  async openRacingPage(): Promise<RacingPage> {
    const racingPage = new RacingPage(this.page);
    await racingPage.open();
    return racingPage;
  }

  async assumeRacingPage(): Promise<RacingPage> {
    const racingPage = new RacingPage(this.page);
    await racingPage.assume();
    return racingPage;
  }
}

export function start(page: Page): Start {
  return new Start(page);
}
