# WSL2 开发环境设置

## :warning: 🚨 **切勿将 meeting-plunger 源码克隆到 Windows 目录（如 `/mnt/c/`）!!!**

请在 WSL2 会话中，先执行 `cd ~`，然后 `git clone git@github.com:your-org/meeting-plunger.git`

## 1. 确保从官方 Microsoft Store 安装 WSL2 和 Ubuntu-24.04

参考这个 [YouTube 视频教程，了解如何安装 WSL2 和 WSLg](https://www.youtube.com/watch?v=FQ6ahcJOVz0)（WSL2 中启用 Linux GUI）。

**重要提示：** 确保不要以 `root` 用户运行 WSL2 进行 meeting-plunger 开发。使用 `root` 用户安装 `nix` 工具会失败！

## 2. 安装 Playwright 和 GUI 支持所需的额外软件包

对于 **Ubuntu 24.04**，安装 Playwright 所需的以下软件包：

```bash
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install -y \
  libgtk2.0-0t64 libgtk-3-0t64 libgbm-dev libnotify-dev libnss3 \
  libxss1 libasound2t64 libxtst6 libatomic1 libatk-bridge2.0-0 \
  libcups2 libdrm2 libgbm1 xauth xvfb curl git
```

对于 **Ubuntu 22.04** 或更早版本：

```bash
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get install -y \
  libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libnss3 \
  libxss1 libasound2 libxtst6 libatomic1 libatk-bridge2.0-0 \
  libcups2 libdrm2 libgbm1 xauth xvfb curl git
```

## 3. Git 配置

### 配置行尾符（检出时保持原样，提交时使用 Unix 风格）

```bash
git config --global core.autocrlf input
```

克隆仓库后，规范化行尾符：

```bash
cd ~/meeting-plunger
git add --renormalize .
```

### Git 凭证

您可以配置 WSL2 Git 使用 Windows 凭据管理器，以避免重复输入个人访问令牌。请参考[这篇文章](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git)进行设置。

## 4. 安装 Nix 包管理器

Meeting Plunger 使用 Nix 来提供可重现的开发环境。运行自动化设置脚本：

```bash
cd ~/meeting-plunger
./setup-meeting-plunger-dev.sh
```

此脚本将：
- 安装 Nix 包管理器（如果尚未安装）
- 配置 Nix flakes
- 设置开发环境

**脚本完成后，请退出终端并打开一个新终端**，以确保 Nix 正确初始化。

## 5. 首次设置

安装依赖：

```bash
cd ~/meeting-plunger
nix develop -c pnpm install && nix develop -c pnpm e2e:install
```

## 6. 验证安装

启动服务（终端 1）：

```bash
nix develop -c pnpm sut
```

运行端到端测试（终端 2）：

```bash
nix develop -c pnpm e2e
```

如果测试通过，说明您的环境已正确设置！🎉

## 7. 以浏览器界面模式运行测试（headed 模式）

要运行带有可见浏览器的 Playwright 测试（headed 模式），您可能需要配置 X-Server：

### 方案 A：使用 WSLg（Windows 11 搭配 WSL2g）

在 Windows 11 上，WSLg 应该开箱即用。只需运行：

```bash
nix develop -c pnpm e2e:headed
```

### 方案 B：使用 VcXsrv（Windows 10 或 WSLg 不工作时）

1. 下载并安装 [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. 配置 XLaunch：
   - 打开开始菜单 > 右键点击 XLaunch 快捷方式 > 更多 > 打开文件位置
   - 在资源管理器窗口中右键点击 XLaunch 快捷方式 > 属性
   - 在目标字段的结尾双引号后添加 `-ac` 选项：
     - 示例：`"C:\Program Files\VcXsrv\xlaunch.exe" -ac`
3. 在运行 headed 测试之前启动 XLaunch

如果 DISPLAY 变量仍有问题，请将以下内容添加到您的 `~/.bashrc`：

```bash
export DISPLAY=$(route.exe print | grep 0.0.0.0 | head -1 | awk '{print $4}'):0.0
```

然后重新加载 shell：

```bash
source ~/.bashrc
```

## 常见问题

### Nix 安装失败

如果自动化设置脚本失败，请参阅 [docs/nix.md](nix.md) 获取详细的手动安装说明。

### Playwright 浏览器安装错误

如果 Playwright 无法下载浏览器，请尝试：

```bash
nix develop -c pnpm e2e:install
```

### 权限被拒绝错误

确保您不是以 `root` 用户运行。检查方法：

```bash
whoami
```

如果返回 `root`，请创建一个新用户并切换到该用户。

## 下一步

请参阅以下文档了解更多详情：

- [QUICK_START.md](QUICK_START.md) - 快速入门指南
- [VSCODE_SETUP.md](VSCODE_SETUP.md) - VSCode + Cucumber 设置
- [VERIFICATION.md](VERIFICATION.md) - 设置验证
- [README.md](../README.md) - 项目概述

## 重要提醒

- **在 Nix shell 外运行命令时，务必使用 `nix develop -c` 前缀**
- 后端代码更改时会自动重新加载（Python FastAPI）
- 客户端代码更改时会自动重新加载（Go with Air）
- 端到端测试需要两个服务都在运行（`pnpm sut`）
- 默认使用无头模式以加快测试执行速度
