import { Page, expect } from '@playwright/test';
import path from 'path';

export class HomePage {
  constructor(private page: Page) {}

  async open(): Promise<this> {
    await this.page.goto('http://localhost:3000');
    return this;
  }

  async assume(): Promise<this> {
    // Verify we're on the home page by checking for the main heading
    const heading = this.page.locator('h1:has-text("Meeting Plunger")');
    await expect(heading).toBeVisible({ timeout: 3000 });
    return this;
  }

  async uploadAudioFile(filename: string): Promise<this> {
    // Find the file upload control (with shorter timeout for clearer error)
    const fileInput = this.page.locator('input[type="file"]');
    await fileInput.waitFor({ timeout: 3000 });

    // Upload the fixture file
    const fixturePath = path.join(process.cwd(), 'fixtures', filename);
    await fileInput.setInputFiles(fixturePath);

    // Click the upload button
    const uploadButton = this.page.locator('button:has-text("Upload")');
    await uploadButton.click();

    return this;
  }

  async verifyTranscript(expectedTranscript: string): Promise<void> {
    const result = this.page.locator('text=' + expectedTranscript);
    await expect(result).toBeVisible();
  }
}
