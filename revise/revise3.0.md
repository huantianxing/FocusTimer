# Revise 3.0 — 前端项目构建日志

**日期**: 2026-06-09  
**分支**: main  
**作者**: heixing

---

## 一、概述

按照 `req.md` 第 5/7 节的设计规范，在 `frontend/` 目录下从零搭建了完整的 Vue 3 前端项目。共计创建 **50 个文件**，涵盖 5 个页面视图、20 个功能组件、5 个 Pinia Store、API 封装层、主题系统、路由系统等。

## 二、技术栈

| 技术 | 版本 | 用途 |
|---|---|---|
| Vue 3 | 3.x (Composition API + `<script setup>`) | 前端框架 |
| Vite | 8.x | 构建工具 + 开发服务器 |
| Element Plus | 最新 | UI 组件库（中文语言包） |
| Pinia | 最新 | 状态管理 |
| Vue Router | 4.x | 前端路由（懒加载） |
| ECharts | 5.x | 数据可视化图表 |
| Axios | 最新 | HTTP 请求封装 |
| SCSS | 最新 | 样式预处理 |

## 三、文件清单

### 3.1 项目配置（4 文件）

| 文件 | 说明 |
|---|---|
| `frontend/index.html` | 入口 HTML，中文 lang，favicon emoji |
| `frontend/vite.config.js` | Vite 配置：`@` 别名 + `/api` 代理到 `127.0.0.1:5000` |
| `frontend/.env.development` | 开发环境变量 |
| `frontend/.env.production` | 生产环境变量 |

### 3.2 样式系统（2 文件）

| 文件 | 说明 |
|---|---|
| `src/styles/theme.css` | CSS 变量定义，浅色/深色双主题（完全照搬 req.md 5.1 节配色规范） |
| `src/styles/global.scss` | 全局 reset、布局（app-layout / app-header / app-body / app-sidebar / app-main）、Element Plus 深色模式覆盖、自定义滚动条 |

### 3.3 工具函数（2 文件）

| 文件 | 关键导出 |
|---|---|
| `src/utils/timeFormat.js` | `formatHHMMSS()`, `formatHumanReadable()`, `formatCompact()`, `formatTimeOnly()`, `formatDateTime()`, `getTodayStr()`, `getDateStrDaysAgo()` |
| `src/utils/chartConfig.js` | `getChartTheme()`, `getAxisConfig()`, `getEChartsThemeName()` |

### 3.4 API 层（1 文件，20 个 API 方法）

| 文件 | 接口覆盖 |
|---|---|
| `src/api/index.js` | 计时（startTimer, pauseTimer, resumeTimer, endTimer, getCurrentTimer） |
| | 记录（getTodayRecords, getRecords, updateRecord, markRecordInvalid） |
| | 统计（getTodayStats, getTrendStats, getTaskRanking） |
| | 标签（getTags, createTag, updateTag, deleteTag） |
| | 设置（getSettings, updateSettings, uploadSound） |
| | 模板（getTemplates, createTemplate, deleteTemplate） |
| | 备份（triggerBackup, getBackupList） |

Axios 拦截器统一处理：成功响应数据提取、4xx/5xx 错误弹出 Element Plus Message 提示。

### 3.5 Pinia Stores（5 文件）

| 文件 | state 核心字段 | 关键 actions |
|---|---|---|
| `src/stores/timer.js` | `currentRecord`, `isRunning`, `elapsedSeconds` | `startPolling()`（1秒轮询 `/api/timer/current`）, `start()`, `pause()`, `resume()`, `end()` |
| `src/stores/records.js` | `todayRecords`, `historyRecords`, `filters` | `fetchTodayRecords()`, `fetchHistoryRecords()` |
| `src/stores/theme.js` | `mode` (system/light/dark), `resolved` | `loadFromSettings()`, `setMode()`, `toggle()`, 系统 `matchMedia` 监听 |
| `src/stores/sound.js` | `enabled`, `volume`, `customSoundPath` | `play(eventType)` — Web Audio API 合成 6 种事件音效 |
| `src/stores/settings.js` | `settings` (全部配置项) | `load()`, `save(partial)` |

### 3.6 Vue Router（1 文件，5 路由）

| 文件 | 路由表 |
|---|---|
| `src/router/index.js` | `/` → HomeView, `/history` → HistoryView, `/stats` → StatsView, `/tags` → TagsView, `/settings` → SettingsView。所有路由懒加载。全局后置守卫设置 `<title>` |

### 3.7 通用组件（3 文件）

| 组件 | 功能 |
|---|---|
| `components/common/AppHeader.vue` | 顶部导航栏：Logo + 应用名 + 今日总时长（实时）+ 主题切换 + 音量控制 + 设置按钮 |
| `components/common/ThemeToggle.vue` | 三态循环按钮：🖥️跟随系统 / ☀️浅色 / 🌙深色（Element Plus Tooltip 提示当前模式） |
| `components/common/SoundControl.vue` | 🔊 图标 + 悬停弹出垂直音量滑块（0-100%，step 5%） |

### 3.8 计时组件（4 文件）

| 组件 | 功能 |
|---|---|
| `components/timer/TimerDisplay.vue` | 大字体计时器（72px, monospace, font-weight:200），实时刷新 `HH:MM:SS`，active=蓝色 paused=橙色 |
| `components/timer/TaskModal.vue` | 开始任务弹窗：标题输入（1-50字符）+ 标签多选 + 快捷模板区（点击一键开始） |
| `components/timer/TimerControls.vue` | 按钮组：空闲→[开始] / 计时中→[暂停][结束] / 已暂停→[继续][结束] |
| `components/timer/PomodoroIndicator.vue` | 番茄钟 4 圆点进度指示器（预留，Phase 5 启用） |

### 3.9 记录组件（3 文件）

| 组件 | 功能 |
|---|---|
| `components/records/RecordList.vue` | 今日记录列表：同标题自动分组、组头显示累计时长、可展开/折叠查看详细记录 |
| `components/records/RecordItem.vue` | 单条记录行：时间范围、时长、状态标签、编辑按钮 |
| `components/records/RecordEditModal.vue` | 编辑弹窗：标题/开始时间/结束时间/标签修改 |

### 3.10 统计组件（5 文件）

| 组件 | 图表类型 | 数据来源 |
|---|---|---|
| `components/stats/TodayOverview.vue` | 4 列统计卡片（无图） | `GET /api/stats/today` |
| `components/stats/HourlyChart.vue` | 24 小时柱状图 | `GET /api/stats/today` → `hourly_data` |
| `components/stats/TaskPieChart.vue` | 环形饼图（Top5）+ 图例 | `GET /api/stats/today` → `pie_data` |
| `components/stats/TrendChart.vue` | 趋势折线图（7/30/90天切换）| `GET /api/stats/trend?range=N` |
| `components/stats/TaskRanking.vue` | 横向条形图 Top10 | `GET /api/stats/tasks?limit=10` |

所有图表组件：自动响应主题切换（浅色/深色 ECharts 主题），监听 `resize` 自适应容器大小，`onUnmounted` 销毁实例防内存泄漏。

### 3.11 设置组件（5 文件）

| 组件 | 功能 |
|---|---|
| `components/settings/ThemeSettings.vue` | 三选一主题模式（el-radio-group + 卡片式选项） |
| `components/settings/SoundSettings.vue` | 音效开关 + 音量滑块 + 预览按钮（开始/暂停/结束）+ 自定义音效上传（el-upload） |
| `components/settings/TimerSettings.vue` | 番茄钟参数：工作时长/短休息/长休息/循环次数（el-input-number） |
| `components/settings/HotkeySettings.vue` | 快捷键展示：开始/暂停（Ctrl+Alt+S）、结束（Ctrl+Alt+E），带 Electron 暂未支持的提示 |
| `components/settings/DataSettings.vue` | 自动备份开关 + 立即备份按钮 + 关于信息（版本/技术栈/数据存储说明） |

### 3.12 页面视图（5 文件）

| 视图 | 布局结构 |
|---|---|
| `views/HomeView.vue` | 双栏布局：主区（计时面板 + 4 卡片 + 图表两列）+ 侧栏（320px 今日记录列表）。挂载时启动轮询 |
| `views/HistoryView.vue` | 筛选工具栏（日期范围/关键词/标签下拉/快捷筛选按钮）+ 分页表格 + 分页组件 |
| `views/StatsView.vue` | 双栏：左侧趋势图 + 右侧任务排行榜 |
| `views/TagsView.vue` | CRUD 表格 + 新建/编辑弹窗（16 色预设色板 + 自定义 hex 输入） |
| `views/SettingsView.vue` | 左侧 Tab 导航（外观/计时/音效/快捷键/数据&关于），右侧对应设置组件 |

### 3.13 核心入口（2 文件）

| 文件 | 说明 |
|---|---|
| `src/main.js` | createApp → Pinia → Router → Element Plus（中文）→ 全局图标注册 → mount |
| `src/App.vue` | 根布局：AppHeader + `<router-view />`，onMounted 初始化设置/主题/音效 |

## 四、关键设计决策

1. **计时轮询机制**：`timer` store `startPolling()` 在 HomeView 挂载时启动 `setInterval` 每秒调 `GET /api/timer/current`，离开页面时 `stopPolling()` 清除。响应式 `elapsedSeconds` 驱动 TimerDisplay 实时刷新。

2. **主题持久化方案**：`theme` store 初始化时优先从 `localStorage` 读取（避免 API 返回前的闪烁），然后异步通过 `GET /api/settings` 获取 `theme_mode` 作为最终数据源。切换时同步写入 `PUT /api/settings` + `localStorage`。

3. **系统主题跟随**：`window.matchMedia('(prefers-color-scheme: dark)')` 监听系统变化，仅在 mode='system' 时响应。

4. **音效系统**：默认使用 Web Audio API 合成短促提示音（无需外部文件），支持自定义上传 MP3/WAV。6 种事件音效：start/pause/end/break_start/break_end/goal_achieved。

5. **CSS 变量主题切换**：`[data-theme="dark"]` 选择器覆盖 CSS 变量，Element Plus 组件通过全局 SCSS 覆盖适配深色模式。

6. **API 错误统一处理**：Axios 响应拦截器统一弹出 `ElMessage` 提示，各组件调用 API 时只需处理成功分支。

## 五、验证结果

```bash
cd frontend
npm install     # 成功安装 111 个依赖包
npx vite build  # ✓ built in 1.30s, 2301 modules transformed
                # 输出: dist/ (index.html + CSS + JS, 无编译错误)
```

- **构建状态**: ✅ 成功
- **模块转换**: 2301 modules
- **页面数量**: 5 个（Home / History / Stats / Tags / Settings）
- **组件数量**: 20 个（3 common + 4 timer + 3 records + 5 stats + 5 settings）
- **Store 数量**: 5 个（timer / records / theme / sound / settings）
- **API 方法**: 20 个（覆盖全部后端接口）

## 六、与后端对接状态

| 后端接口 | 前端调用位置 | 状态 |
|---|---|---|
| `POST /api/timer/start` | `timer.js` store → `TaskModal.vue` | ✅ |
| `POST /api/timer/pause` | `timer.js` store → `TimerControls.vue` | ✅ |
| `POST /api/timer/resume` | `timer.js` store → `TimerControls.vue` | ✅ |
| `POST /api/timer/end` | `timer.js` store → `TimerControls.vue` | ✅ |
| `GET /api/timer/current` | `timer.js` store（polling） | ✅ |
| `GET /api/records/today` | `records.js` → `RecordList.vue` | ✅ |
| `GET /api/records` | `records.js` → `HistoryView.vue` | ✅ |
| `PUT /api/records/:id` | `RecordEditModal.vue` | ✅ |
| `POST /api/records/:id/invalid` | API 已封装，组件中预留 | ⚪ |
| `GET /api/stats/today` | `TodayOverview.vue`, `HourlyChart.vue`, `TaskPieChart.vue` | ✅ |
| `GET /api/stats/trend` | `TrendChart.vue` | ✅ |
| `GET /api/stats/tasks` | `TaskRanking.vue` | ✅ |
| `GET/POST /api/tags` | `TagsView.vue` | ✅ |
| `PUT/DELETE /api/tags/:id` | `TagsView.vue` | ✅ |
| `GET/PUT /api/settings` | `settings.js`, `theme.js`, `sound.js` | ✅ |
| `POST /api/settings/sound` | `SoundSettings.vue` | ✅ |
| `GET/POST /api/templates` | `TaskModal.vue` | ✅ |
| `DELETE /api/templates/:id` | API 已封装 | ⚪ |
| `GET /api/backup` | `DataSettings.vue` | ✅ |

## 七、后续待完成

1. **Electron 桌面端封装**（Phase 5+）：系统托盘、全局快捷键、窗口管理
2. **番茄钟自动循环**（Phase 5）：25min 专注 → 自动提示休息 → 恢复
3. **全局快捷键实际绑定**（Phase 5）：Electron 主进程注册
4. **前端单元测试**：Vitest + Vue Test Utils
5. **E2E 测试**：Playwright / Cypress
6. **i18n 国际化**：Vue I18n（预留中文/English 切换）
