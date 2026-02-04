# VSCode Configuration

This directory contains shared VSCode settings for the Meeting Plunger project.

## Files

- **`settings.json`** - Workspace settings including Cucumber/Gherkin configuration
- **`extensions.json`** - Recommended extensions
- **`launch.json`** - Debug configurations
- **`tasks.json`** - Task runner configurations

## Recommended Extensions

When you open this project in VSCode, you'll be prompted to install the recommended extensions. These include:

### Essential Extensions

1. **Cucumber (Gherkin) Full Support**
   - Author: Alexander Krechik (`alexkrechik.cucumberautocomplete`)
   - Features:
     - Step definition autocomplete
     - Go to definition
     - Syntax highlighting for `.feature` files

2. **Cucumber Official**
   - Author: Cucumber (`cucumber.cucumber-official`)
   - Official Cucumber support

3. **Playwright Test for VSCode**
   - Author: Microsoft (`ms-playwright.playwright`)
   - Run and debug Playwright tests

### Language Support

4. **Python** - Python language support
5. **Pylance** - Fast Python language server
6. **Black Formatter** - Python code formatter
7. **Go** - Go language support
8. **ESLint** - JavaScript linting
9. **Prettier** - Code formatter

### Optional but Useful

10. **GitLens** - Enhanced Git capabilities
11. **Code Spell Checker** - Spell checking in code
12. **EditorConfig** - Consistent coding styles

## Cucumber Configuration

The `settings.json` file is configured to help VSCode find your step definitions:

```json
{
  "cucumber.features": ["e2e/features/**/*.feature"],
  "cucumber.glue": [
    "e2e/steps/**/*.js",
    "e2e/support/**/*.js"
  ]
}
```

### Features

- **Autocomplete**: Type steps in `.feature` files and get suggestions from existing step definitions
- **Go to Definition**: Ctrl+Click (Cmd+Click on Mac) on a step to jump to its implementation
- **Validation**: Real-time validation of Gherkin syntax
- **Parameter Highlighting**: Parameters like `{string}` and `{int}` are highlighted

## Debug Configurations

### 1. Python: FastAPI

Debug the backend FastAPI application.

**Usage:**
1. Open `backend/main.py`
2. Set breakpoints
3. Press F5 or use "Python: FastAPI" configuration
4. Backend starts on http://localhost:8000

### 2. Go: Client

Debug the Go client application.

**Usage:**
1. Open `client/main.go`
2. Set breakpoints
3. Press F5 or use "Go: Client" configuration
4. Client starts on http://localhost:3000

### 3. E2E: Debug Tests

Debug E2E tests with Playwright.

**Usage:**
1. Open a test file in `e2e/`
2. Set breakpoints in step definitions
3. Press F5 or use "E2E: Debug Tests" configuration
4. Browser opens in debug mode (PWDEBUG=1)

### 4. Full Stack (Compound)

Debug both backend and client simultaneously.

**Usage:**
1. Select "Full Stack" from debug dropdown
2. Press F5
3. Both services start in debug mode

## Tasks

Available tasks (Ctrl+Shift+P → "Tasks: Run Task"):

- **Start SUT (Backend + Client)** - Run `pnpm sut`
- **Run E2E Tests** - Run `pnpm e2e`
- **Run E2E Tests (Headed)** - Run `pnpm e2e:headed`
- **Start Backend** - Start backend only
- **Start Client** - Start client only
- **Install Dependencies** - Install all dependencies

### Quick Access

- Press `Ctrl+Shift+B` (or `Cmd+Shift+B` on Mac) for quick task access

## Using Cucumber Features in VSCode

### Writing Feature Files

1. Create a new `.feature` file in `e2e/features/`
2. Start typing a scenario
3. VSCode will suggest existing steps
4. Use snippets like `Feature:`, `Scenario:`, `Given`, `When`, `Then`

### Navigating to Step Definitions

1. Open a `.feature` file
2. Ctrl+Click (Cmd+Click on Mac) on any step
3. VSCode jumps to the step definition in `e2e/steps/`

### Finding Step Usage

1. Open a step definition file
2. Right-click on a step definition
3. Select "Find All References"
4. See all `.feature` files using this step

### Autocomplete

When typing in a `.feature` file:
```gherkin
Given I open the client
```
VSCode suggests:
- `Given I open the client application at "http://localhost:3000"`

## Language-Specific Settings

### Python

- **Formatter**: Black (88 character line length)
- **Linter**: Flake8
- **Format on Save**: Enabled
- **Organize Imports on Save**: Enabled

### Go

- **Formatter**: gofmt
- **Format on Save**: Enabled
- **Organize Imports on Save**: Enabled

### JavaScript

- **Formatter**: Prettier
- **Format on Save**: Enabled
- **Linter**: ESLint

### Gherkin (.feature files)

- **Format on Save**: Disabled (to preserve intentional formatting)

## Troubleshooting

### Step Definitions Not Found

If VSCode can't find step definitions:

1. Check that paths in `settings.json` are correct:
   ```json
   "cucumber.glue": [
     "e2e/steps/**/*.js",
     "e2e/support/**/*.js"
   ]
   ```

2. Reload VSCode window:
   - Ctrl+Shift+P → "Developer: Reload Window"

3. Ensure Cucumber extension is installed:
   - Ctrl+Shift+X → Search for "Cucumber"

### Autocomplete Not Working

1. Check file is saved with `.feature` extension
2. Ensure step definitions exist in `e2e/steps/`
3. Try restarting the Cucumber language server:
   - Ctrl+Shift+P → "Cucumber: Regenerate autocomplete"

### Debug Configuration Not Working

1. Ensure dependencies are installed:
   ```bash
   pnpm install
   pnpm e2e:install
   ```

2. Check that services aren't already running on those ports
3. View Debug Console for error messages

## Tips

1. **Quick Open**: Use `Ctrl+P` (Cmd+P on Mac) to quickly open files
   - Type `@` to see symbols in current file
   - Type `#` to search in workspace

2. **Multi-Cursor**: Hold Alt (Option on Mac) and click to add cursors

3. **Column Selection**: Hold Alt+Shift (Option+Shift on Mac) and drag

4. **Command Palette**: `Ctrl+Shift+P` (Cmd+Shift+P on Mac) for all commands

5. **Integrated Terminal**: Use `Ctrl+`` to toggle terminal

6. **Split Editor**: Drag files to split view

## Customization

Feel free to customize these settings for your local environment:

1. Create `.vscode/settings.local.json` (git-ignored)
2. Override any settings from `settings.json`
3. VSCode will merge both files

Example `.vscode/settings.local.json`:
```json
{
  "editor.fontSize": 14,
  "workbench.colorTheme": "Dark+ (default dark)"
}
```

## More Information

- [VSCode Cucumber Extension](https://marketplace.visualstudio.com/items?itemName=alexkrechik.cucumberautocomplete)
- [Playwright Extension](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright)
- [VSCode Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [VSCode Tasks](https://code.visualstudio.com/docs/editor/tasks)
