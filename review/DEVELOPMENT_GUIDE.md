# TimerFocus 项目架构与开发指南

> 本文档面向后续开发，说明项目结构、数据流转、各文件职责，以及新增功能的标准开发流程。

---

## 一、项目总览

```
TimerFocus/
├── backend/                    # Flask 后端 (Python)
│   ├── run.py                  # ★ 启动入口
│   ├── config.py               # 全局配置
│   ├── requirements.txt        # Python 依赖
│   └── app/
│       ├── __init__.py         # ★ Flask 工厂 + 路由注册 + 静态文件托管
│       ├── config.py           # 配置类（开发/生产/测试）
│       ├── models.py           # ★ 数据库表定义（6 张表）
│       ├── routes/             # ★ API 路由层（接收请求 → 调 service → 返回 JSON）
│       ├── services/           # ★ 业务逻辑层（核心逻辑，不碰 HTTP）
│       └── utils/              # 工具函数（校验、数据库工具）
├── frontend/                   # Vue 3 前端
│   ├── index.html              # HTML 入口
│   ├── src/
│   │   ├── main.js             # ★ Vue 初始化
│   │   ├── App.vue             # ★ 根组件（布局骨架）
│   │   ├── router/index.js     # ★ 路由表（5 个页面）
│   │   ├── api/index.js        # ★ 所有后端 API 封装
│   │   ├── stores/             # ★ Pinia 状态管理（5 个 store）
│   │   ├── views/              # 页面组件（5 个页面）
│   │   ├── components/         # 可复用组件（按功能分组）
│   │   ├── styles/             # 全局样式 + CSS 变量
│   │   └── utils/              # 工具函数
│   └── dist/                   # 构建产物（npm run build 生成）
├── build_exe.bat               # 一键打包脚本
├── revise/                     # 开发日志
└── review/                     # 本文档
```

---

## 二、架构分层（三层设计）

```
┌─────────────────────────────────────────────────┐
│                  前端 (Vue 3)                     │
│  views → components → stores → api/index.js     │
│                          ↓ HTTP (axios)          │
└─────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────┐
│               后端路由层 (routes/)                │
│  职责：接收请求 → 参数校验 → 调 service → 返 JSON  │
│  不直接操作数据库                                  │
└─────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────┐
│              业务逻辑层 (services/)               │
│  职责：核心业务逻辑、数据库操作、状态管理            │
│  不依赖 HTTP 请求上下文                            │
└─────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────┐
│              数据层 (models.py)                   │
│  职责：定义表结构、to_dict() 序列化                 │
│  使用 SQLAlchemy ORM                              │
└─────────────────────────────────────────────────┘
                           ↓
                    SQLite 数据库
```

**铁律**：前端永远不直接调数据库，必须走 `组件 → store → api → 后端路由 → service → model → 数据库`。

---

## 三、后端详细说明

### 3.1 启动流程

```
双击 .exe (或 python run.py)
  → run.py
    → import webview（顶层，PyInstaller 需要）
    → from backend.app import create_app
    → create_app() 工厂函数:
        1. 读取 config.py 配置
        2. 初始化数据库 db.init_app(app)
        3. 配置 CORS（允许跨域）
        4. 注册 API 路由 (register_api_routes)
        5. 注册静态文件路由 (register_static_routes) — 仅生产模式
        6. 创建表 db.create_all()
        7. 初始化默认数据（5 个默认标签 + 默认设置）
    → 根据 --mode 参数:
        dev    → app.run(debug=True)  标准 Flask 开发服务器
        desktop → 后台线程跑 Flask + PyWebView 桌面窗口
```

### 3.2 文件职责速查

| 文件 | 一句话职责 |
|------|-----------|
| `backend/config.py` | 全局配置常量（数据库路径、备份路径、默认值） |
| `backend/app/config.py` | 环境配置类（Development / Production / Testing） |
| `backend/app/__init__.py` | Flask 工厂函数 + 路由注册 + 静态文件托管 + 默认数据初始化 |
| `backend/app/models.py` | 6 张数据库表的 SQLAlchemy 定义 |
| `backend/app/routes/timer.py` | 计时 API：开始/暂停/继续/结束/查询当前 |
| `backend/app/routes/records.py` | 记录 API：今日记录/历史记录/编辑/标记无效 |
| `backend/app/routes/stats.py` | 统计 API：今日概览/趋势/任务排行 |
| `backend/app/routes/tags.py` | 标签 API：增删改查 |
| `backend/app/routes/settings.py` | 设置 API：读取/更新设置 + 音效上传 |
| `backend/app/routes/templates.py` | 模板 API：增删查 |
| `backend/app/routes/backup.py` | 备份 API：手动触发 + 备份列表 |
| `backend/app/services/timer_service.py` | 计时核心逻辑（全局状态管理 + 数据库操作） |
| `backend/app/services/stats_service.py` | 统计计算逻辑 |
| `backend/app/services/backup_service.py` | 备份文件操作 |
| `backend/app/services/sound_service.py` | 音效文件管理 |
| `backend/app/utils/validators.py` | 输入校验函数 |
| `backend/app/utils/database.py` | 数据库工具函数 |
| `backend/app/utils/backup.py` | 备份底层操作 |
| `backend/tests/` | 单元测试（conftest.py 配置测试 Fixture） |

### 3.3 数据库表（6 张）

| 表名 | 模型类 | 用途 |
|------|--------|------|
| `timer_records` | `TimerRecord` | 计时任务记录（核心表） |
| `tags` | `Tag` | 标签（名称 + 颜色） |
| `daily_stats` | `DailyStats` | 每日统计缓存 |
| `operation_logs` | `OperationLog` | 操作日志 |
| `user_settings` | `UserSettings` | 用户设置（单用户，id=1） |
| `task_templates` | `TaskTemplate` | 快捷任务模板 |

### 3.4 API 接口总览

```
POST   /api/timer/start         开始计时  { title, tag_ids }
POST   /api/timer/pause         暂停计时
POST   /api/timer/resume        继续计时
POST   /api/timer/end           结束计时
GET    /api/timer/current       查询当前计时状态

GET    /api/records/today       今日记录（分组）
GET    /api/records             历史记录（分页+筛选）
PUT    /api/records/:id         修改记录
POST   /api/records/:id/invalid 标记无效

GET    /api/stats/today         今日统计（时长/任务数/时段/饼图）
GET    /api/stats/trend?range=7 趋势数据
GET    /api/stats/tasks?limit=10 任务排行

GET    /api/tags                标签列表
POST   /api/tags                创建标签
PUT    /api/tags/:id            修改标签
DELETE /api/tags/:id            删除标签

GET    /api/settings            获取设置
PUT    /api/settings            更新设置
POST   /api/settings/sound      上传音效

GET    /api/templates           模板列表
POST   /api/templates           创建模板
DELETE /api/templates/:id       删除模板

GET    /api/backup              手动备份
GET    /api/backup/list         备份列表
```

所有接口统一返回格式：`{ code: 200, message: 'ok', data: {...} }`

---

## 四、前端详细说明

### 4.1 启动流程

```
npm run dev (开发) 或 双击 .exe (生产)
  → main.js
    → createApp(App)
    → use(Pinia)         状态管理
    → use(Router)        路由
    → use(ElementPlus)   UI 组件库
    → 注册所有 Element Plus 图标
    → import './styles/theme.css'    CSS 变量
    → import './styles/global.scss'  全局样式
    → mount('#app')
```

### 4.2 路由表

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | `HomeView.vue` | 主页：计时面板 + 图表 + 侧边栏 |
| `/history` | `HistoryView.vue` | 历史记录：筛选 + 分页表格 |
| `/stats` | `StatsView.vue` | 统计分析：趋势图 + 排行榜 |
| `/tags` | `TagsView.vue` | 标签管理：增删改查 |
| `/settings` | `SettingsView.vue` | 设置：主题/计时/音效/快捷键/数据 |

### 4.3 Pinia Store 职责

| Store | 文件 | 管理的状态 |
|-------|------|-----------|
| `useTimerStore` | `stores/timer.js` | 当前计时记录、运行状态、1 秒轮询 |
| `useRecordsStore` | `stores/records.js` | 今日记录列表、历史记录、分页 |
| `useSettingsStore` | `stores/settings.js` | 用户设置（从 API 加载/保存） |
| `useThemeStore` | `stores/theme.js` | 主题模式（system/light/dark），挂载到 `<html data-theme>` |
| `useSoundStore` | `stores/sound.js` | 音效开关/音量/播放 |

### 4.4 组件树

```
App.vue
├── AppHeader.vue                导航栏（Logo + 5 个链接 + 音效 + 主题）
└── <router-view>
    ├── HomeView.vue
    │   ├── TimerDisplay.vue     大号计时数字
    │   ├── PomodoroIndicator.vue 番茄钟圆点
    │   ├── TimerControls.vue    开始/暂停/继续/结束按钮
    │   │   └── TaskModal.vue    开始任务弹窗（标题 + 标签 + 模板）
    │   ├── TodayOverview.vue    4 张统计卡片
    │   ├── HourlyChart.vue      24 小时柱状图
    │   ├── TaskPieChart.vue     任务占比饼图
    │   └── RecordList.vue       今日记录分组列表
    │       ├── RecordItem.vue   单条记录行
    │       └── RecordEditModal.vue 编辑弹窗
    ├── HistoryView.vue          筛选栏 + 分页表格
    ├── StatsView.vue
    │   ├── TrendChart.vue       趋势折线图
    │   └── TaskRanking.vue      任务排行横向条形图
    ├── TagsView.vue             标签表格 + 新建/编辑弹窗
    └── SettingsView.vue
        ├── ThemeSettings.vue    外观（system/light/dark）
        ├── TimerSettings.vue    番茄钟参数
        ├── SoundSettings.vue    音效开关/音量/上传
        ├── HotkeySettings.vue   快捷键配置
        └── DataSettings.vue     备份 + 关于
```

### 4.5 文件职责速查

| 文件 | 一句话职责 |
|------|-----------|
| `src/main.js` | Vue 应用入口，注册插件 |
| `src/App.vue` | 根组件：AppHeader + router-view |
| `src/router/index.js` | 5 条路由定义 |
| `src/api/index.js` | 所有后端 API 封装（axios 实例 + 拦截器 + 19 个导出函数） |
| `src/stores/timer.js` | 计时状态：轮询、开始/暂停/继续/结束 |
| `src/stores/records.js` | 记录状态：今日列表、历史列表、分页 |
| `src/stores/settings.js` | 设置状态：加载、保存 |
| `src/stores/theme.js` | 主题状态：切换、持久化 |
| `src/stores/sound.js` | 音效状态：开关、音量、播放 |
| `src/styles/theme.css` | CSS 变量（颜色、圆角、阴影、间距、字体） |
| `src/styles/global.scss` | 全局样式（布局、卡片、滚动条、Element Plus 覆盖、动画） |
| `src/utils/timeFormat.js` | 时间格式化函数 |
| `src/utils/chartConfig.js` | ECharts 主题配置 |

---

## 五、数据流转详解（以"开始计时"为例）

这是整个项目最核心的流程，理解它就理解了全部架构：

```
用户点击 [开始计时] 按钮
  │
  ▼
TimerControls.vue                  showTaskModal = true → 弹出 TaskModal
  │
  ▼
TaskModal.vue                      用户输入标题 + 选择标签
  │  emit('started')
  ▼
TimerControls.vue                  onTaskModalStarted()
  │  emit('started')
  ▼
HomeView.vue                       recordsStore.fetchTodayRecords()
  │
  ▼
TaskModal.vue                      handleStart()
  │  timerStore.start({ title, tag_ids })
  ▼
stores/timer.js                    timerStore.start()
  │  apiStart({ title, tag_ids })      ← 调用 API 封装函数
  ▼
api/index.js                       startTimer()
  │  api.post('/timer/start', {...})   ← axios POST 请求
  ▼
══════════════ 网络 ══════════════════════════════
  ▼
backend/app/routes/timer.py        TimerAPI._start()
  │  1. 获取 JSON 参数
  │  2. validate_title(title)         ← 校验
  │  3. start_timer(title, tags)      ← 调 service
  ▼
backend/app/services/timer_service.py   start_timer()
  │  1. 检查是否已有进行中任务
  │  2. 创建 TimerRecord → db.session.add()
  │  3. 创建 OperationLog
  │  4. db.session.commit()
  │  5. 更新全局状态 current_timer
  │  6. 返回 record.to_dict()
  ▼
══════════════ 网络 ══════════════════════════════
  ▼
stores/timer.js                    收到响应
  │  currentRecord.value = res.data
  │  isRunning.value = true
  │  startPolling()                  ← 启动 1 秒轮询
  ▼
TimerDisplay.vue                   每 1 秒更新 elapsedSeconds
  │  formatHHMMSS(elapsedSeconds) → "00:05:32"
  ▼
用户看到计时器在跑
```

---

## 六、新增功能标准开发流程

假设你想加一个 **"每日目标"** 功能（设置每天专注 X 小时，首页显示进度条）。

### 第 1 步：数据库（后端）

**文件**：`backend/app/models.py`

```python
# 在 UserSettings 表中加字段
class UserSettings(db.Model):
    ...
    daily_goal_minutes = db.Column(db.Integer, default=120)  # 新增

    def to_dict(self):
        return {
            ...
            'daily_goal_minutes': self.daily_goal_minutes,   # 新增
        }
```

### 第 2 步：API 接口（后端）

设置接口已经支持动态更新（PUT `/api/settings`），不需要改路由层。

如果需要新接口（比如 `GET /api/stats/progress`），在 `routes/stats.py` 加一个 Resource 类，然后在 `app/__init__.py` 的 `register_api_routes()` 注册。

### 第 3 步：前端 API 封装

**文件**：`frontend/src/api/index.js`

```javascript
// 不需要新增，getSettings() 和 updateSettings() 已覆盖
```

### 第 4 步：前端 Store

**文件**：`frontend/src/stores/settings.js`

SettingsStore 已经自动包含新字段，无需修改。

### 第 5 步：前端 UI

**文件**：`frontend/src/components/stats/TodayOverview.vue`（加一个进度条卡片）

```vue
<!-- 新增第 5 张卡片 -->
<div class="overview-card card">
  <div class="card-icon">🎯</div>
  <div class="card-info">
    <div class="card-title">今日目标</div>
    <el-progress :percentage="progressPercent" />
  </div>
</div>
```

### 总结：开发顺序

```
1. models.py          → 加数据库字段
2. routes/ + services → 加 API 接口（如需新接口）
3. api/index.js       → 封装前端 API 调用
4. stores/            → 加状态管理逻辑
5. views/ + components/ → 写 UI 组件
6. npm run build      → 构建前端
7. build_exe.bat      → 打包测试
```

**黄金法则**：从数据层往 UI 层写。先让后端能存、能查，再让前端能展示。

---

## 七、常见开发场景速查

| 想做什么 | 改哪些文件 |
|----------|-----------|
| 加一个设置项 | `models.py` → SettingStore 自动生效 |
| 加一个统计图表 | `routes/stats.py` → `services/stats_service.py` → `api/index.js` → 新 `components/stats/XxxChart.vue` |
| 加一个页面 | `router/index.js` → 新 `views/XxxView.vue` → `AppHeader.vue`（加导航链接） |
| 改 UI 样式 | `styles/theme.css`（变量）+ `styles/global.scss`（全局）+ 组件 scoped style |
| 改计时逻辑 | `services/timer_service.py` |
| 加一个数据库表 | `models.py` → `routes/` + `services/` |
| 修改配色 | `styles/theme.css`（改 CSS 变量值） |
| 加一个新 API | `routes/xxx.py` → `app/__init__.py`（register_api_routes 注册） |
| 改页面布局 | `views/XxxView.vue` 或 `components/` |

---

## 八、关键约定与注意事项

1. **统一响应格式**：所有 API 返回 `{ code, message, data }`，前端拦截器据此处理
2. **路由层不写业务逻辑**：routes 只做参数校验 + 调 service + 包装返回值
3. **Service 层不依赖 HTTP**：函数参数和返回值都是纯 Python 对象
4. **CSS 变量优先**：颜色/圆角/阴影/间距都用 `var(--xxx)`，不写硬编码值
5. **前后端分离开发**：`npm run dev`（Vite） + `python run.py`（Flask），通过 CORS 通信
6. **打包前必须构建前端**：`npm run build` 生成 `frontend/dist/`，PyInstaller 才能打包
7. **不要改 backend 目录下的 `run.py` 的 import webview 位置**：必须在顶层，否则打包失败
8. **图标必须是真 .ico**：不是 png 改后缀，Pillow 会自动转换
9. **窗口默认 1200×800**：设计 UI 时确保关键按钮在这个尺寸下可见
