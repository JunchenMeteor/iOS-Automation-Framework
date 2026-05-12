# iOS-Automation-Framework Implementation Roadmap

本文合并并替代根目录临时草稿 `iOS-Automation-Framework-Optimization.md` 与 `iOS-Automation-Framework-WebUI.md`。它用于记录当前完成度、仍应保留的设计原则，以及近 / 中 / 远期实现方向。

## 当前结论

最新 `upstream/main` 已经完成原 Web UI 方案的大部分 MVP 内容：本地 FastAPI Web UI、文件浏览、环境检查、白名单测试执行、SSE 日志、Allure run 级报告、mock/Claude AI 问答、依赖声明、README 入口和 GitHub Actions API 测试都已经存在。

后续不应再按两份旧草稿从零实现 Web UI，而应把重点放在验证、补齐文档、降低运行风险、增强 AI 检索质量、完善 macOS UI 测试闭环和平台集成稳定性上。

## 已完成内容评估

| 原计划项 | 当前状态 | 证据 / 说明 |
|---|---|---|
| `pytest-xdist` 并发能力 | 已完成 | `requirements.txt` 包含 `pytest-xdist~=3.8.0`，`pytest.ini` 默认 `-n auto`。平台与 UI 命令使用 `-n 0` 保持稳定。 |
| Appium 2.x 明确化 | 已完成 | `requirements.txt` 注明 Appium 2.x，README 要求 Node.js 18+、Appium 2.x 和 XCUITest driver。 |
| 元素定位策略优化 | 部分完成 | Page Object 已大量使用 Accessibility ID、Predicate、Class Chain；但 README 仍提到 XPath，部分变量名仍为 `_XPATH` 但实际使用 Predicate，需要清理命名和文档。 |
| GitHub Actions API CI | 已完成基础版 | `.github/workflows/ci.yml` 会在 push / PR 运行 API 测试并上传 Allure/JUnit 结果；当前 `continue-on-error: true` 更像证据收集，不是严格质量门。 |
| 依赖版本明确 | 部分完成 | 多数依赖使用 `==` 或 `~=`；尚未引入 `pip-compile` 或锁文件。 |
| 一键启动脚本 | 已完成基础版 | `run_api.*` 和 `run_ui.*` 存在；但不支持参数化模块/环境，且 `run_ui.bat` 使用 `taskkill /f /im node.exe`，风险较高。 |
| Docker 支持 | 未完成 | 没有 `docker-compose.yml`。iOS UI 自动化依赖 macOS/Xcode，Docker 不适合作为完整 UI 执行方案。 |
| README 真实化 | 已完成基础版 | README 已覆盖结构、运行方式、Web UI、mock API、平台集成和限制；仍可继续补截图/GIF 和实测结果。 |
| Web UI 基础服务 | 已完成 | `tools/webui/app.py` 提供 FastAPI 入口、静态首页、健康检查和 API 路由。 |
| 文件树与安全读取 | 已完成基础版 | `file_service.py` 使用白名单、忽略目录、敏感文件/扩展名过滤和 200KB 限制。 |
| 环境检查 | 已完成基础版 | `env_service.py` 检查 Python、pytest、Allure、Appium、Xcode、API/UI 可运行性。 |
| 测试模块白名单 | 已完成 | `run_service.py` 固定 `api_all`、`api_smoke`、`api_regression`、`ui_all`、`ui_smoke`，不接受任意命令。 |
| 测试执行、日志、取消、超时 | 已完成基础版 | 使用 `asyncio.create_subprocess_exec`，SSE 推送日志，支持取消和超时。 |
| Allure run 级报告 | 已完成基础版 | 结果写入 `Reports/webui-runs/{run_id}`，避免覆盖固定目录。 |
| AI 问答 | 已完成基础版 | 支持 mock 答复和 Claude 可选接入；当前检索是关键词映射，不是完整索引。 |
| Web UI 前端 | 已完成基础版 | `tools/webui/static/index.html` 使用 Alpine.js，无前端构建链路。 |
| Windows API 验证 | 待持续执行 | 已具备 mock API 和 API smoke 路径；每次修改后仍应用本机命令重新验证。 |
| macOS UI 验证 | 未完成 | 需要 macOS + Xcode + Appium + iOS Simulator + `APP_PATH`。 |

## 保留的设计原则

以下原则仍然有效，后续实现应继续遵守：

- Web UI 是本地单用户 demo console，不是生产级测试平台。
- 前端只传模块 ID，后端只执行白名单命令。
- 不使用 `shell=True` 执行测试命令。
- iOS UI 测试默认串行执行，固定 `-n 0`，避免设备/模拟器冲突。
- Windows/Linux 可以开发 Web UI 和运行 API 测试，但 iOS UI 执行必须明确提示需要 macOS + Xcode + Appium。
- 报告使用 run 级目录 `Reports/webui-runs/{run_id}`，不能覆盖 `Reports/api-report` 或 `Reports/ui-report`。
- 不读取 `.env`、`config/local.yml`、证书、密钥、profile 等敏感文件。
- 日志输出必须脱敏 token、Authorization、password、api_key、secret 等字段。
- AI 回答必须基于项目上下文；上下文不足时说明不确定，并给出建议查看的文件。
- 不让 Web UI 自动安装 Xcode/Appium/Allure。
- 如果后续需要自动启动 Appium，只能关闭自己启动的进程，不能杀全部 `node.exe`。

## 近期目标

近期目标用于把已落地功能从“能跑”推进到“可验证、可维护、可演示”。

1. 补齐 Web UI 专属文档。
   - 新增或完善 `tools/webui/README.md`。
   - 说明启动命令、环境变量、mock AI、Claude 可选接入、报告目录、Windows/macOS 边界。

2. 固化 Windows API 验证流程。
   - 使用 `tools.mock_api.server` 启动本地 mock API。
   - 设置 `API_BASE_URL=http://127.0.0.1:8010`。
   - 验证 `api_smoke` 在 CLI 和 Web UI 中都能执行并产生报告。
   - 将实测命令和结果写入 README 或 Web UI README。

3. 修正 pytest timeout 配置。
   - `pytest.ini` 已配置 `timeout`，但 `requirements.txt` 当前未显式包含 `pytest-timeout`。
   - 二选一：加入 `pytest-timeout`，或移除无效配置并改由 Web UI 超时控制负责。

4. 清理 UI locator 命名和文档。
   - 将实际使用 Predicate 的 `_XPATH` 变量改名为 `_PREDICATE` 或 `_FALLBACK`。
   - README 中“XPath”改为“XPath 仅作为最后兜底”，与当前实现一致。
   - 保留定位优先级：Accessibility ID > Predicate > Class Chain > XPath。

5. 降低一键 UI 脚本风险。
   - 避免 `run_ui.bat` 中 `taskkill /f /im node.exe` 杀掉所有 Node 进程。
   - 改成记录自己启动的 Appium 进程并只关闭该进程，或要求用户手动启动 Appium。

6. 调整 CI 质量门策略。
   - 明确 `.github/workflows/ci.yml` 中 `continue-on-error: true` 是证据收集还是临时容错。
   - 如果目标是 PR 质量门，应让 API smoke 失败时阻断合并。

7. 补充 Web UI 基础测试。
   - 覆盖文件白名单、敏感路径拒绝、模块白名单、日志脱敏、run metadata 恢复。
   - 优先用 pytest 测服务层，不急于做浏览器自动化。

## 中期目标

中期目标用于增强 Web UI 和平台集成能力，但仍保持本地 demo 的边界。

1. 增强 AI 检索。
   - 从关键词映射升级为轻量分块检索。
   - 回答引用文件路径，最好能定位到行号。
   - 支持对 README、pytest.ini、Page Object、API case、config 的优先检索。

2. 完善任务运行模型。
   - 区分“测试失败”和“Allure 报告生成失败”。
   - 记录 report generation 状态和错误信息。
   - 为取消任务补齐子进程组处理，避免 Windows/macOS 行为不一致。

3. 增强 Web UI 交互。
   - 日志自动滚动可暂停。
   - 历史 run 更清晰地展示状态、耗时、模块和报告链接。
   - 环境不满足时提供明确的修复建议，而不仅是禁用按钮。

4. 与 `meteortest.yml` 保持一致。
   - Web UI 模块和 `meteortest.yml` suite 不应长期分叉。
   - 后续可从 `meteortest.yml` 读取安全 suite 列表，再附加 Web UI 运行约束。

5. macOS UI 测试验证。
   - 在 macOS 上验证 `ui_smoke`。
   - 检查 Xcode、simctl、Appium Server、XCUITest driver、`APP_PATH` 的真实状态。
   - 把 macOS 验证步骤写入 README 和 Web UI README。

6. 依赖锁定策略。
   - 如果项目需要可重复安装，评估 `pip-tools`。
   - 生成并维护 `requirements.lock.txt` 或等价锁文件。

## 远期目标

远期目标只有在本地 demo 稳定后再推进，避免过早扩大复杂度。

1. 运行趋势和历史分析。
   - 基于 `Reports/webui-runs` 汇总通过率、失败模块、耗时和 flaky 倾向。
   - 保留最近 N 次运行并提供清理策略。

2. 更完整的 AI 助手。
   - 建立文件索引或符号索引。
   - 支持基于失败日志、Allure 结果、测试代码的失败分析。
   - 生成建议时明确引用证据，不编造项目状态。

3. 性能测试入口。
   - 第一阶段只展示 Locust 目录和文档。
   - 后续如加入 `perf_locust_headless`，必须固定参数、默认小流量、明确风险，不能让前端传任意压测目标和并发。

4. Docker / Dev Container。
   - Docker 可以用于 API 测试、mock API、Web UI 的开发环境。
   - 不应承诺 Docker 能完整运行 iOS UI 自动化，因为 Xcode 和 iOS Simulator 依赖 macOS。

5. 多用户和远程执行。
   - 当前 Web UI 不做多用户权限、云端设备池或分布式队列。
   - 如果未来需要，应优先由 MeteorTest 平台承担调度、权限、审计和执行器管理，而不是把本仓库 Web UI 扩展成生产平台。

## 不再保留的旧表述

以下旧草稿内容不应继续作为真实状态引用：

- “Web UI 待从零实现”的描述：当前 `tools/webui` 已存在。
- “当前最新提交为 a0175e6”的描述：这是旧扫描结果，不能作为当前仓库状态。
- “步骤 1-16 全部完成”的笼统表述：应拆成本文的具体完成度表，避免掩盖验证缺口。
- “添加 docker-compose 一条命令启动 Appium + 测试环境”的完整承诺：iOS UI 自动化不能被 Docker 一条命令完整覆盖。
- “补充真实截图/GIF 演示”作为高优先级实现项：可以作为文档增强，但不应优先于验证和安全边界。

## 推荐下一步

优先做近期目标 1 到 3：

1. 补 `tools/webui/README.md`。
2. 跑通 Windows mock API + Web UI `api_smoke` 实测并记录。
3. 处理 `pytest-timeout` 配置与依赖不一致。

这三项能把当前已实现的 Web UI 从代码状态推进到可复现演示状态，收益最高，风险最低。
