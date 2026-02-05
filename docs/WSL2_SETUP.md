# WSL2 Development Environment Setup

## :warning: 🚨 **DO NOT CLONE meeting-plunger source to a MS Windows directory (e.g. `/mnt/c/`)!!!**

Instead, in your WSL2 session, `cd ~` then `git clone git@github.com:your-org/meeting-plunger.git`

## 1. Ensure you install WSL2 with Ubuntu-24.04 from official Microsoft Store

Follow this [YouTube video tutorial on how to install WSL2 with WSLg](https://www.youtube.com/watch?v=FQ6ahcJOVz0) (Linux GUI enabled in WSL2).

**Important:** Make sure you do not run WSL2 as `root` user for meeting-plunger development environment. The `nix` tool setup with `root` user will fail!

## 2. Additional packages for Playwright and GUI support

For **Ubuntu 24.04**, install the following packages required by Playwright:

```bash
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install -y \
  libgtk2.0-0t64 libgtk-3-0t64 libgbm-dev libnotify-dev libnss3 \
  libxss1 libasound2t64 libxtst6 libatomic1 libatk-bridge2.0-0 \
  libcups2 libdrm2 libgbm1 xauth xvfb curl git
```

For **Ubuntu 22.04** or earlier:

```bash
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install -y \
  libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libnss3 \
  libxss1 libasound2 libxtst6 libatomic1 libatk-bridge2.0-0 \
  libcups2 libdrm2 libgbm1 xauth xvfb curl git
```

## 3. Git configuration

### Configure line endings (checkout as-is, commit Unix-style)

```bash
git config --global core.autocrlf input
```

After cloning the repository, normalize line endings:

```bash
cd ~/meeting-plunger
git add --renormalize .
```

### Git credentials

You can configure WSL2 Git to use Windows Credential Manager to avoid entering personal access tokens repeatedly. Follow [this article](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git) for setup instructions.

## 4. Install Nix package manager

Meeting Plunger uses Nix for reproducible development environments. Run the automated setup script:

```bash
cd ~/meeting-plunger
./setup-meeting-plunger-dev.sh
```

This script will:
- Install Nix package manager (if not already installed)
- Configure Nix flakes
- Set up the development environment

**After the script completes, exit your terminal and open a new one** to ensure Nix is properly initialized.

## 5. First-time setup

Install dependencies:

```bash
cd ~/meeting-plunger
nix develop -c pnpm install && nix develop -c pnpm e2e:install
```

## 6. Verify installation

Start the services (Terminal 1):

```bash
nix develop -c pnpm sut
```

Run E2E tests (Terminal 2):

```bash
nix develop -c pnpm e2e
```

If tests pass, your environment is set up correctly! 🎉

## 7. Running tests with browser UI (headed mode)

To run Playwright tests with the browser visible (headed mode), you may need to configure an X-Server:

### Option A: Using WSLg (Windows 11 with WSL2g)

WSLg should work out of the box on Windows 11. Just run:

```bash
nix develop -c pnpm e2e:headed
```

### Option B: Using VcXsrv (Windows 10 or if WSLg doesn't work)

1. Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Configure XLaunch:
   - Open your start menu > right-click XLaunch shortcut > More > Open file location
   - Right-click XLaunch shortcut in the Explorer window > Properties
   - Add `-ac` option right after the closing double quote in the Target field:
     - Example: `"C:\Program Files\VcXsrv\xlaunch.exe" -ac`
3. Start XLaunch before running headed tests

If you still have issues with the DISPLAY variable, add this to your `~/.bashrc`:

```bash
export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0
```

Then reload your shell:

```bash
source ~/.bashrc
```

## Common Issues

### Nix installation fails

If the automated setup script fails, see [docs/nix.md](nix.md) for detailed manual installation instructions.

### Playwright browser installation errors

If Playwright fails to download browsers, try:

```bash
nix develop -c pnpm e2e:install
```

### Permission denied errors

Make sure you're not running as `root` user. Check with:

```bash
whoami
```

If it returns `root`, create a new user and switch to it.

## Next Steps

See the following documentation for more details:

- [QUICK_START.md](QUICK_START.md) - Quick start guide
- [VSCODE_SETUP.md](VSCODE_SETUP.md) - VSCode + Cucumber setup
- [VERIFICATION.md](VERIFICATION.md) - Setup verification
- [README.md](../README.md) - Project overview

## Important Reminders

- **ALWAYS prefix commands with `nix develop -c`** when running from outside the Nix shell
- Backend auto-reloads on changes (Python FastAPI)
- Client auto-reloads on changes (Go with Air)
- E2E tests require both services running (`pnpm sut`)
- Use headless mode by default for faster test execution
