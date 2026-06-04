---

# 桌面计时器软件需求说明书（修订版 v1.1）

**修订日期**: 2026-06-04  
**修订内容**: 确认单用户模式、本地存储、音效提醒、深色模式支持

---

## 1. 项目概述

### 1.1 项目背景
基于番茄工作法（Pomodoro Technique）理念，开发一款**单用户桌面端**专注计时工具，帮助用户记录和管理个人时间分配，通过数据可视化提升工作效率。所有数据**本地存储**，无需网络连接。

### 1.2 技术架构
- **前端**: Vue 3 + Vite + Element Plus
- **后端**: Python Flask + Flask-RESTful
- **数据库**: SQLite（单用户本地文件存储）
- **通信**: RESTful API + JSON（本地服务）
- **部署**: 桌面端封装方案（Electron ）
- **音效**: Web Audio API 或本地音频文件播放

---

## 2. 功能需求

### 2.1 核心计时功能（FR-001 ~ FR-007）

| 需求编号   | 需求名称     | 详细描述                                                     | 优先级 |
| ---------- | ------------ | ------------------------------------------------------------ | ------ |
| **FR-001** | 任务标题输入 | 点击"开始计时"后，弹出模态框要求输入任务标题（必填，1-50字符）。支持从历史记录快速选择已有标题（自动补全下拉框）。输入框自动聚焦 | P0     |
| **FR-002** | 计时控制     | 提供开始、暂停、继续、结束四个操作按钮。计时精度为秒级，显示格式为 `HH:MM:SS`。按钮状态根据当前计时状态动态变化 | P0     |
| **FR-003** | 实时状态显示 | 计时过程中页面顶部固定显示当前任务标题、已用时间、开始时间。支持窗口最小化到系统托盘后台运行，托盘图标显示进行中的任务名和已用时间 | P1     |
| **FR-004** | 自动保存机制 | 点击"结束"或"暂停超过30分钟"自动保存当前记录。异常关闭（如断电、程序崩溃）时，下次启动检测未正常结束的记录，提示用户恢复或丢弃 | P1     |
| **FR-005** | 番茄钟模式   | 可选开启标准番茄钟模式：25分钟专注 + 5分钟短休息，每4个番茄后15分钟长休息。自动循环提示，可自定义时长参数 | P2     |
| **FR-006** | 快捷操作     | 支持全局快捷键（如 `Ctrl+Alt+S` 开始/暂停，`Ctrl+Alt+E` 结束）。支持系统托盘右键菜单快速开始/暂停/结束 | P2     |
| **FR-007** | 音效提醒     | **计时开始、暂停、结束、番茄钟休息开始/结束时播放提示音**。支持开启/关闭音效、调节音量。提供默认音效，支持用户自定义上传音频文件（MP3/WAV，最大5MB） | P1     |

### 2.2 数据记录与管理（FR-008 ~ FR-013）

| 需求编号   | 需求名称         | 详细描述                                                     | 优先级 |
| ---------- | ---------------- | ------------------------------------------------------------ | ------ |
| **FR-008** | 记录列表展示     | 主页显示今日所有计时记录，包括：任务标题、标签、开始时间、结束时间、持续时长、状态（完成/中断）。相同标题任务自动合并显示，组头显示累计时长 | P0     |
| **FR-009** | 历史记录查询     | 支持按日期范围、任务标题关键词、标签筛选查询。支持分页展示（每页20条）。提供"最近7天"、"本月"、"上月"快捷筛选按钮 | P0     |
| **FR-010** | 记录编辑修正     | 允许修改记录的标题、开始/结束时间（防止误操作），修改需记录到操作日志。不允许删除已完成的记录，可标记为"无效"并备注原因 | P1     |
| **FR-011** | 相同任务合并统计 | 对相同标题的任务，自动汇总当日/当周/当月的总耗时。在列表中显示"该任务今日已累计X小时X分钟"。点击可展开查看详细记录 | P0     |
| **FR-012** | 数据导入导出     | 支持将记录导出为 CSV/Excel/JSON 格式。支持从文件导入历史数据（自动去重合并，冲突时提示用户选择覆盖或跳过） | P2     |
| **FR-013** | 自动本地备份     | 自动每日备份 SQLite 数据库文件到用户指定目录（默认：`~/FocusTimer/backups/`），保留最近30天备份，超期自动清理。支持手动一键备份 | P2     |

### 2.3 统计与可视化（FR-014 ~ FR-018）

| 需求编号   | 需求名称     | 详细描述                                                     | 优先级 |
| ---------- | ------------ | ------------------------------------------------------------ | ------ |
| **FR-014** | 今日概览卡片 | 首页顶部显示4个统计卡片：今日总专注时长、完成任务数、最长连续专注时间、当前进行中的任务（如有） | P0     |
| **FR-015** | 日视图图表   | 柱状图展示今日各时段（每小时）的专注时间分布。饼图展示今日各任务类型的时间占比。图表支持鼠标悬停查看详细数据 | P0     |
| **FR-016** | 周/月趋势图  | 折线图展示最近7天/30天的每日总专注时长趋势。支持同比上周/上月数据。X轴为日期，Y轴为时长（小时） | P1     |
| **FR-017** | 任务排名统计 | 排行榜展示指定时间范围内耗时最长的Top10任务。支持按任务标签分类统计。显示任务占比百分比条 | P1     |
| **FR-018** | 专注质量分析 | 统计中断次数、平均单次专注时长、番茄完成率等效率指标。提供"本周效率评分"（算法：基于完成率、连续专注时长计算） | P2     |

### 2.4 任务标签与分类（FR-019 ~ FR-021）

| 需求编号   | 需求名称     | 详细描述                                                     | 优先级 |
| ---------- | ------------ | ------------------------------------------------------------ | ------ |
| **FR-019** | 标签管理     | 为任务添加自定义标签（如"学习"、"工作"、"阅读"），支持标签颜色设置（16色预设+自定义色板）。一个任务可关联多个标签。标签名称唯一，最多10个字符 | P1     |
| **FR-020** | 预设任务模板 | 支持保存常用任务模板（标题+标签+预计时长），在"开始计时"弹窗中显示"快速开始"区域，一键启动常用任务 | P2     |
| **FR-021** | 任务目标设定 | 可为任务类型/标签设置每日/每周目标时长（如"学习"每日目标4小时），达成后首页显示庆祝动画和音效，进度条实时显示完成度 | P2     |

### 2.5 深色模式支持（FR-022 ~ FR-024）

| 需求编号   | 需求名称          | 详细描述                                                     | 优先级 |
| ---------- | ----------------- | ------------------------------------------------------------ | ------ |
| **FR-022** | 深色/浅色模式切换 | 支持深色模式（Dark Mode）和浅色模式（Light Mode）切换。提供三种选项：**跟随系统**（默认）、**强制浅色**、**强制深色**。切换即时生效无刷新 | P1     |
| **FR-023** | 深色模式配色方案  | 深色模式配色：背景 `#1a1a2e`、卡片 `#16213e`、主文字 `#eaeaea`、次要文字 `#a0a0a0`、强调色 `#0f3460`、成功 `#e94560`、图表配色适配深色对比度 | P1     |
| **FR-024** | 模式持久化        | 用户选择的主题模式保存到 `user_settings` 表（SQLite），下次启动自动恢复。系统跟随模式下，实时监听系统主题变化并自动切换。`user_settings` 表为所有运行时设置的唯一数据源 | P2     |

---

## 3. 数据库设计（SQLite）

### 3.1 数据表结构

```sql
-- 任务记录主表
CREATE TABLE timer_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    tag_ids VARCHAR(255),              -- 关联标签ID（逗号分隔）
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration_seconds INTEGER DEFAULT 0,
    status TINYINT DEFAULT 0,          -- 0:进行中 1:已完成 2:已暂停 3:已中断 4:已标记无效
    is_pomodoro TINYINT DEFAULT 0,
    pomodoro_count INTEGER DEFAULT 0,
    is_deleted TINYINT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 标签表
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(20) NOT NULL UNIQUE,
    color VARCHAR(7) DEFAULT '#409EFF',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 每日统计缓存表（加速查询）
CREATE TABLE daily_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_date DATE NOT NULL UNIQUE,
    total_seconds INTEGER DEFAULT 0,
    task_count INTEGER DEFAULT 0,
    top_task_title TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 操作日志表
CREATE TABLE operation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id INTEGER,
    action VARCHAR(20) NOT NULL,      -- start/pause/resume/end/edit/mark_invalid
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    details TEXT
);

-- 用户设置表（单用户配置）
CREATE TABLE user_settings (
    id INTEGER PRIMARY KEY CHECK (id = 1),  -- 强制只有一条记录
    theme_mode VARCHAR(20) DEFAULT 'system', -- system/light/dark
    sound_enabled TINYINT DEFAULT 1,
    sound_volume INTEGER DEFAULT 80,         -- 0-100
    custom_sound_path VARCHAR(255),          -- 自定义音效路径
    pomodoro_work_minutes INTEGER DEFAULT 25,
    pomodoro_short_break INTEGER DEFAULT 5,
    pomodoro_long_break INTEGER DEFAULT 15,
    pomodoro_cycles INTEGER DEFAULT 4,
    auto_backup_enabled TINYINT DEFAULT 1,
    backup_path VARCHAR(255),
    global_hotkey_start VARCHAR(50) DEFAULT 'Ctrl+Alt+S',
    global_hotkey_end VARCHAR(50) DEFAULT 'Ctrl+Alt+E',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 任务模板表
CREATE TABLE task_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    tag_ids VARCHAR(255),
    estimated_minutes INTEGER,
    sort_order INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. API 接口设计（Flask）

### 4.1 统一响应格式

所有接口均使用以下 JSON 响应信封：

```json
// 成功响应
{ "code": 200, "message": "ok", "data": { ... } }

// 客户端错误
{ "code": 400, "message": "任务标题不能为空", "data": null }

// 服务端错误
{ "code": 500, "message": "服务器内部错误", "data": null }
```

常用错误码：`400` 参数校验失败、`404` 资源不存在、`409` 冲突（如重复标题的标签）、`413` 上传文件过大、`422` 业务逻辑错误（如结束一个已结束的记录）。

### 4.2 接口列表

| 方法   | 路径                       | 功能                 | 请求参数                                                     |
| ------ | -------------------------- | -------------------- | ------------------------------------------------------------ |
| POST   | `/api/timer/start`         | 开始计时             | `title`(必填), `tag_ids`(可选), `is_pomodoro`(可选)          |
| POST   | `/api/timer/pause`         | 暂停计时             | `record_id`                                                  |
| POST   | `/api/timer/resume`        | 继续计时             | `record_id`                                                  |
| POST   | `/api/timer/end`           | 结束计时             | `record_id`                                                  |
| GET    | `/api/timer/current`       | 获取当前进行中的计时 | 无                                                           |
| GET    | `/api/records/today`       | 获取今日记录         | 无                                                           |
| GET    | `/api/records`             | 查询历史记录         | `start_date`, `end_date`, `keyword`, `tag_id`, `page`, `size` |
| PUT    | `/api/records/:id`         | 修改记录             | `title`(可选), `tag_ids`(可选), `start_time`(可选), `end_time`(可选) |
| POST   | `/api/records/:id/invalid` | 标记记录无效         | `reason`(可选)                                               |
| GET    | `/api/stats/today`         | 今日统计数据         | 无                                                           |
| GET    | `/api/stats/trend`         | 趋势数据             | `range`(7/30/90), `group_by`(day/week)                       |
| GET    | `/api/stats/tasks`         | 任务统计排名         | `start_date`, `end_date`, `limit`(默认10)                    |
| GET    | `/api/tags`                | 获取所有标签         | 无                                                           |
| POST   | `/api/tags`                | 创建标签             | `name`, `color`                                              |
| PUT    | `/api/tags/:id`            | 修改标签             | `name`, `color`                                              |
| DELETE | `/api/tags/:id`            | 删除标签             | 无                                                           |
| GET    | `/api/settings`            | 获取用户设置         | 无                                                           |
| PUT    | `/api/settings`            | 更新用户设置         | 各配置项                                                     |
| POST   | `/api/settings/sound`      | 上传自定义音效       | `file`(multipart)                                            |
| GET    | `/api/templates`           | 获取任务模板         | 无                                                           |
| POST   | `/api/templates`           | 创建模板             | `title`, `tag_ids`, `estimated_minutes`                      |
| GET    | `/api/backup/auto`         | 触发手动备份         | 无                                                           |
| GET    | `/api/export/records`      | 导出记录             | `format`(csv/excel/json), `start_date`, `end_date`           |

### 4.3 音效相关接口

```json
// GET /api/settings
Response:
{
  "code": 200,
  "data": {
    "sound_enabled": true,
    "sound_volume": 80,
    "custom_sound_path": null,  // 使用默认音效
    "theme_mode": "system"
  }
}

// PUT /api/settings
Request:
{
  "sound_enabled": false,
  "sound_volume": 60,
  "theme_mode": "dark"
}

// POST /api/settings/sound
// Content-Type: multipart/form-data
// file: [用户上传的MP3/WAV文件]
Response:
{
  "code": 200,
  "data": {
    "custom_sound_path": "/path/to/custom_sound.mp3",
    "message": "音效上传成功"
  }
}
```

---

## 5. 前端页面设计（Vue 3 + 深色模式）

### 5.1 主题配置（CSS Variables）

```css
/* styles/theme.css */
:root {
  /* 浅色模式（默认） */
  --bg-primary: #f5f7fa;
  --bg-card: #ffffff;
  --bg-hover: #f0f2f5;
  --text-primary: #303133;
  --text-secondary: #606266;
  --text-muted: #909399;
  --border-color: #dcdfe6;
  --primary-color: #409eff;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --chart-bg: #ffffff;
}

[data-theme="dark"] {
  /* 深色模式 */
  --bg-primary: #1a1a2e;
  --bg-card: #16213e;
  --bg-hover: #0f3460;
  --text-primary: #eaeaea;
  --text-secondary: #a0a0a0;
  --text-muted: #6c757d;
  --border-color: #2a2a4a;
  --primary-color: #4cc9f0;
  --success-color: #52b788;
  --warning-color: #ffb703;
  --danger-color: #e94560;
  --chart-bg: #16213e;
}
```

### 5.2 页面结构

```
├── 主布局 (MainLayout)
│   ├── 顶部导航栏
│   │   ├── Logo + 应用名称
│   │   ├── 今日总时长（实时更新）
│   │   ├── 主题切换按钮（☀️/🌙/🖥️ 三态）
│   │   ├── 音量控制按钮（🔊 悬停调节滑块）
│   │   └── 设置入口
│   ├── 左侧边栏
│   │   ├── 今日记录列表（按任务标题分组，可折叠）
│   │   ├── 快捷标签筛选（彩色标签云）
│   │   └── 任务模板快速开始区
│   └── 主内容区（HomeView）
│       ├── 计时控制面板
│       │   ├── 大字体计时器（font-size: 72px, font-weight: 200, monospace）
│       │   ├── 当前任务标题（进行中时高亮显示）
│       │   ├── 操作按钮组：开始 / 暂停 / 继续 / 结束
│       │   └── 番茄钟进度指示器（4个圆点表示第几个番茄）
│       ├── 今日概览卡片（4列网格）
│       │   ├── 总专注时长 ⏱️
│       │   ├── 完成任务数 ✅
│       │   ├── 最长连续专注 🎯
│       │   └── 进行中任务 ▶️（或休息中 ☕）
│       ├── 图表区域（两列布局）
│       │   ├── 时段分布柱状图（24小时X轴，0-60分钟Y轴）
│       │   └── 任务占比饼图/环形图（Top5 + 其他）
│       └── 记录列表表格
│           ├── 表头：时间 | 任务 | 标签 | 时长 | 状态 | 操作
│           ├── 相同任务合并行（可展开）
│           └── 编辑/标记无效按钮
│
├── 历史记录页 (HistoryView)
│   ├── 筛选工具栏
│   │   ├── 日期范围选择器（快捷：最近7天/本月/上月/自定义）
│   │   ├── 关键词搜索框（实时过滤）
│   │   ├── 标签多选筛选器
│   │   └── 导出按钮（CSV/Excel/JSON下拉选择）
│   └── 分页表格（支持排序、列宽调整）
│
├── 统计分析页 (StatsView)
│   ├── 时间范围切换（7日/30日/90日）
│   ├── 趋势折线图（双Y轴：时长 + 任务数）
│   ├── 任务排行榜（横向条形图，Top10）
│   └── 效率指标面板（完成率、中断率、平均时长、效率评分）
│
├── 标签管理页 (TagsView)
│   └── 标签CRUD表格（颜色选择器、使用次数统计）
│
└── 设置页 (SettingsView)
    ├── 外观设置
    │   ├── 主题模式：跟随系统 / 浅色 / 深色（单选按钮组）
    │   └── 界面语言（预留：中文/English）
    ├── 计时设置
    │   ├── 番茄钟参数：工作时长/短休息/长休息/循环次数（数字输入框）
    │   └── 自动暂停阈值（默认30分钟，可关闭）
    ├── 音效设置
    │   ├── 开启/关闭音效（开关）
    │   ├── 音量滑块（0-100%，实时预览）
    │   ├── 音效选择：默认提示音 / 自定义上传
    │   └── 各事件独立开关（开始/结束/休息开始/休息结束）
    ├── 快捷键设置
    │   ├── 开始/暂停：Ctrl+Alt+S（可修改，检测冲突）
    │   └── 结束计时：Ctrl+Alt+E（可修改）
    ├── 数据管理
    │   ├── 数据库文件位置显示（只读）
    │   ├── 自动备份：开启/关闭、备份路径、保留天数
    │   ├── 立即备份按钮
    │   ├── 导入数据（支持CSV/JSON/Excel）
    │   └── 导出全部数据
    └── 关于
        ├── 版本信息
        ├── 开源协议
        └── 数据存储说明（本地SQLite，隐私安全）
```

### 5.3 深色模式视觉规范

| 元素       | 浅色模式  | 深色模式                                   |
| ---------- | --------- | ------------------------------------------ |
| 页面背景   | `#f5f7fa` | `#1a1a2e`                                  |
| 卡片背景   | `#ffffff` | `#16213e`                                  |
| 卡片边框   | `#e4e7ed` | `#2a2a4a`                                  |
| 主要文字   | `#303133` | `#eaeaea`                                  |
| 次要文字   | `#606266` | `#a0a0a0`                                  |
| 禁用文字   | `#c0c4cc` | `#6c757d`                                  |
| 主按钮     | `#409eff` | `#4cc9f0`                                  |
| 成功状态   | `#67c23a` | `#52b788`                                  |
| 危险状态   | `#f56c6c` | `#e94560`                                  |
| 图表网格线 | `#ebeef5` | `#2a2a4a`                                  |
| 悬停背景   | `#f5f7fa` | `#0f3460`                                  |
| 滚动条     | 系统默认  | 自定义深色（`#4a4a6a`轨道，`#6a6a8a`滑块） |

---

## 6. 音效系统设计

### 6.1 默认音效事件

| 事件     | 默认音效                        | 播放时机                         |
| -------- | ------------------------------- | -------------------------------- |
| 计时开始 | 清脆的"叮"声（C5音符，0.3秒）   | 用户点击开始并确认标题后         |
| 计时暂停 | 柔和的"咚"声（降调，0.2秒）     | 用户点击暂停时                   |
| 计时结束 | 愉悦的完成音效（和弦，0.8秒）   | 用户点击结束或番茄钟工作阶段完成 |
| 休息开始 | 轻松的提示音（上升音阶，0.5秒） | 番茄钟休息阶段开始时             |
| 休息结束 | 轻快的提醒音（0.5秒）           | 番茄钟休息阶段结束时             |
| 目标达成 | 庆祝音效（小旋律，1.5秒）       | 当日某标签目标时长达成时         |

### 6.2 音效文件管理

> **音效文件来源**：默认音效可通过两种方式获取——(1) 使用 Web Audio API 用代码合成短促提示音（无需外部文件），(2) 从免费音效库（如 freesound.org、pixabay.com）下载符合规格的 MP3 文件。推荐方案 (1) 用于默认音效以减少资源依赖，方案 (2) 作为自定义音效的参考。

```
backend/
├── static/
│   └── sounds/
│       ├── start_default.mp3
│       ├── pause_default.mp3
│       ├── end_default.mp3
│       ├── break_start_default.mp3
│       ├── break_end_default.mp3
│       └── goal_achieved_default.mp3
```

### 6.3 前端音效播放实现

```javascript
// 使用 Web Audio API 或 HTML5 Audio
// stores/sound.js (Pinia)
export const useSoundStore = defineStore('sound', {
  state: () => ({
    enabled: true,
    volume: 0.8,
    customSounds: {},
    audioContext: null
  }),
  
  actions: {
    async play(eventType) {
      if (!this.enabled) return;
      
      const soundPath = this.customSounds[eventType] 
        || `/static/sounds/${eventType}_default.mp3`;
      
      const audio = new Audio(soundPath);
      audio.volume = this.volume;
      await audio.play();
    },
    
    // 预加载音效避免延迟
    preload() {
      const events = ['start', 'pause', 'end', 'break_start', 'break_end'];
      events.forEach(type => {
        const audio = new Audio(`/static/sounds/${type}_default.mp3`);
        audio.load();
      });
    }
  }
});
```

---

## 7. 项目目录结构（更新版）

```
focus-timer/
├── backend/                          # Flask 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── models.py                  # SQLAlchemy 模型
│   │   ├── config.py                  # 配置管理
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── timer.py               # 计时接口
│   │   │   ├── records.py             # 记录管理
│   │   │   ├── stats.py               # 统计数据
│   │   │   ├── tags.py                # 标签管理
│   │   │   ├── settings.py            # 用户设置
│   │   │   └── templates.py           # 任务模板
│   │   ├── services/
│   │   │   ├── timer_service.py
│   │   │   ├── stats_service.py
│   │   │   ├── backup_service.py
│   │   │   └── sound_service.py       # 音效文件管理
│   │   └── utils/
│   │       ├── database.py            # DB连接/迁移
│   │       ├── backup.py              # 自动备份逻辑
│   │       └── validators.py          # 参数校验
│   ├── static/
│   │   └── sounds/                    # 默认音效文件
│   ├── migrations/                    # 数据库迁移（Flask-Migrate）
│   ├── instance/
│   │   └── focus_timer.db             # SQLite数据库（运行时生成）
│   ├── config.py                      # 全局配置
│   ├── requirements.txt
│   └── run.py                         # 启动入口
│
├── frontend/                          # Vue 3 前端
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   │   └── sounds/                # 前端备用音效（开发用）
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── ThemeToggle.vue    # 主题切换按钮（☀️/🌙/🖥️）
│   │   │   │   ├── SoundControl.vue   # 音量控制（悬停滑块）
│   │   │   │   └── AppHeader.vue      # 顶部导航栏
│   │   │   ├── timer/
│   │   │   │   ├── TimerDisplay.vue   # 大字体计时器
│   │   │   │   ├── TaskModal.vue      # 开始任务弹窗（含自动补全）
│   │   │   │   ├── TimerControls.vue  # 开始/暂停/结束按钮组
│   │   │   │   └── PomodoroIndicator.vue  # 番茄钟进度点
│   │   │   ├── records/
│   │   │   │   ├── RecordList.vue     # 记录列表（分组折叠）
│   │   │   │   ├── RecordItem.vue     # 单条记录行
│   │   │   │   └── RecordEditModal.vue # 编辑弹窗
│   │   │   ├── stats/
│   │   │   │   ├── TodayOverview.vue  # 今日概览4卡片
│   │   │   │   ├── HourlyChart.vue    # 时段分布柱状图
│   │   │   │   ├── TaskPieChart.vue   # 任务占比饼图
│   │   │   │   ├── TrendChart.vue     # 趋势折线图
│   │   │   │   └── TaskRanking.vue    # 任务排行榜
│   │   │   └── settings/
│   │   │       ├── ThemeSettings.vue   # 主题设置
│   │   │       ├── SoundSettings.vue   # 音效设置（含上传）
│   │   │       ├── TimerSettings.vue   # 计时参数设置
│   │   │       ├── HotkeySettings.vue  # 快捷键设置
│   │   │       └── DataSettings.vue    # 数据备份/导入导出
│   │   ├── router/
│   │   │   └── index.js               # Vue Router 路由定义（含导航守卫）
│   │   ├── views/
│   │   │   ├── HomeView.vue           # 首页（计时+今日概览+图表）
│   │   │   ├── HistoryView.vue        # 历史记录
│   │   │   ├── StatsView.vue          # 统计分析
│   │   │   ├── TagsView.vue           # 标签管理
│   │   │   └── SettingsView.vue       # 设置（分标签页）
│   │   ├── stores/                    # Pinia 状态管理
│   │   │   ├── timer.js               # 计时状态（当前记录、时间）
│   │   │   ├── records.js             # 记录列表状态
│   │   │   ├── theme.js               # 主题模式状态
│   │   │   ├── sound.js               # 音效设置状态
│   │   │   └── settings.js            # 用户设置状态
│   │   ├── api/
│   │   │   └── index.js               # Axios封装 + API方法
│   │   ├── composables/
│   │   │   ├── useTimer.js            # 计时逻辑组合式函数
│   │   │   ├── useTheme.js            # 主题切换逻辑
│   │   │   └── useSound.js            # 音效播放逻辑
│   │   ├── styles/
│   │   │   ├── theme.css              # CSS变量定义
│   │   │   └── global.scss            # 全局样式
│   │   ├── utils/
│   │   │   ├── timeFormat.js          # 时间格式化工具
│   │   │   └── chartConfig.js         # 图表主题配置（深浅色适配）
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── .env.development                  # 开发环境变量
│   ├── .env.production                   # 生产环境变量
│   └── vite.config.js                    # 需配置 server.proxy 将 /api 代理到 Flask 后端
│
├── electron/                            # Electron 桌面端（Phase 5+）
│   ├── main.js                           # 主进程（窗口管理、系统托盘、全局快捷键）
│   ├── preload.js                        # 预加载脚本（安全暴露 IPC）
│   └── tray.js                           # 托盘图标与菜单
│
├── tests/                               # 测试
│   ├── backend/
│   │   ├── test_timer.py
│   │   ├── test_records.py
│   │   ├── test_stats.py
│   │   └── test_tags.py
│   └── frontend/
│       ├── components/
│       └── stores/
│
├── docs/                              # 文档
│   └── requirements.md                # 本需求说明书
│
├── scripts/                           # 辅助脚本
│   └── build.py                       # 打包脚本
│
└── README.md
```

---

## 8. 开发阶段规划（更新）

| 阶段        | 周期  | 交付内容                                                     |
| ----------- | ----- | ------------------------------------------------------------ |
| **Phase 1** | 1-2周 | 核心计时功能、任务标题输入、今日记录列表、SQLite数据库、基础REST API |
| **Phase 2** | 1周   | 历史查询、记录编辑、标签管理、相同任务合并显示、数据导出     |
| **Phase 3** | 1周   | **深色模式实现**（CSS变量、主题切换、系统跟随）、**音效系统**（默认音效、音量控制） |
| **Phase 4** | 1-2周 | 统计图表（日/周/月）、任务排名、效率评分、趋势分析           |
| **Phase 5** | 1周   | 番茄钟模式、系统托盘、全局快捷键、自动备份                   |
| **Phase 6** | 1周   | 任务模板、目标设定、自定义音效上传、UI细节优化、打包测试     |

---

## 9. 附录

### 9.1 确认的配置清单

| 配置项   | 确认状态 | 说明                                             |
| -------- | -------- | ------------------------------------------------ |
| 用户模式 | ✅ 单用户 | 无需登录，本地SQLite存储                         |
| 云同步   | ❌ 不需要 | 纯本地工具，无网络同步                           |
| 音效提醒 | ✅ 需要   | 6种事件音效，支持开关、音量调节、自定义上传      |
| 深色模式 | ✅ 需要   | 跟随系统/强制浅色/强制深色三态切换，完整配色方案 |

### 9.2 音效文件规格
- **格式**: MP3 (优先) / WAV
- **采样率**: 44.1kHz
- **码率**: 128kbps（MP3）
- **时长**: 默认音效 0.2-1.5秒
- **文件大小**: 单个文件 < 500KB，自定义上传限制 5MB
- **播放方式**: 前端 HTML5 Audio API，支持预加载

### 9.3 主题切换技术方案
- **实现方式**: CSS 自定义属性（Variables）+ `data-theme` 属性切换
- **持久化**: 前端 `localStorage` 缓存即时生效，同时通过 `PUT /api/settings` 写入 `user_settings` 表作为持久存储。启动时后端返回设置，前端以此为最终数据源
- **系统跟随**: 监听 `window.matchMedia('(prefers-color-scheme: dark)')` 变化事件
- **图表适配**: ECharts 主题配置动态切换（`dark` / `light` 主题对象）
- **Element Plus**: 使用 `el-config-provider` 的 `theme` 属性或 CSS 变量覆盖

---

