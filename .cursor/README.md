# Cursor Configuration

This directory contains Cursor AI rules for the project.

## Files

- **`rules/general.mdc`** - Essential project rules and workflow
  - Nix command prefix requirement
  - Quick commands for development
  - Project structure overview
  - Development workflow
- **`rules/tdd-and-commits.mdc`** - TDD 与 Git 提交规范
  - TDD 流程：先写测试（红）→ 最小实现（绿）→ 必要时重构
  - 按计划小步提交，提交信息格式与不提交未通过测试的代码
- **`rules/e2e-testing.mdc`** - E2E testing (Playwright + Cucumber)，匹配 `e2e/**/*` 时应用

## Key Rule

**ALWAYS prefix commands with `nix develop -c`**

See [`rules/general.mdc`](rules/general.mdc) for complete details.
