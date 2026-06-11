# 架构重构文档 v1.0

**日期**: 2026-06-05  
**重构范围**: 后端 Python Flask 项目，从「Routes 直连数据库」改为「Routes → Services → Models」三层分离

---

## 1. 重构动机

### 问题：重构前

```
前端 Vue
  ↓ HTTP
Routes（收请求 + 业务逻辑 + 写 SQL + 返回 JSON  ← 全塞在一起）
  ↓
Models / SQLite 数据库
```

- `routes/timer.py` 268行，包含请求解析、数据库创建、日志写入、时间计算所有代码
- `routes/stats.py` 172行，包含复杂的聚合计算和嵌套循环
- 4 个 `services/` 文件全是空的（timer_service/stats_service/backup_service/sound_service）
- 业务逻辑无法复用：如果 Electron 托盘也要调用结束计时，需要复制代码
- 无法单独测试业务逻辑：测试任何功能都要启动 Flask

### 目标：重构后

```
前端 Vue
  ↓ HTTP
Routes（只做三件事：收参数 → 调 service → 返回 JSON）
  ↓
Services（所有业务逻辑、数据库操作在这里）
  ↓
Models / SQLite 数据库
```

---

## 2. 修改文件清单

### 新建文件（1个）

| 文件 | 说明 |
|------|------|
| `backend/app/routes/backup.py` | 备份 API 路由（新增 `/api/backup` 和 `/api/backup/list`） |

### 重写文件（6个）

| 文件 | 修改前 | 修改后 |
|------|--------|--------|
| `services/timer_service.py` | 空文件（1行） | 6个函数，220行：计时核心逻辑 + 运行时状态管理 |
| `services/stats_service.py` | 空文件（1行） | 3个函数，150行：今日统计/趋势/排名聚合 |
| `services/backup_service.py` | 空文件（1行） | 5个函数，100行：备份/清理/列表 |
| `services/sound_service.py` | 空文件（1行） | 4个函数，110行：音效校验/保存/路径管理 |
| `routes/timer.py` | 268行（业务+DB+请求混在一起） | 65行（只做参数解析和转发） |
| `routes/stats.py` | 172行（聚合计算在 route 里） | 45行（只做参数解析和转发） |

### 修改文件（4个）

| 文件 | 变更内容 |
|------|---------|
| `routes/settings.py` | `SoundUploadAPI` 改为调用 `sound_service.save_sound_file()`，移除 TODO |
| `routes/templates.py` | 拆出 `TemplateDetailAPI` 类，新增正确的 `delete(template_id)` 方法 |
| `app/__init__.py` | 注册 `TemplateDetailAPI`、`BackupAPI`、`BackupListAPI` 三条新路由 |
| `app/services/__init__.py` | 无需修改（原本不存在，不影响） |

### 未修改的文件（保持原样）

| 文件 | 保留原因 |
|------|---------|
| `routes/records.py` | 记录 CRUD 逻辑相对简单直接，且涉及复杂的分组和筛选展示逻辑，可后续再抽 |
| `routes/tags.py` | 标签操作很薄，基本就是参数校验 + 数据库读写，抽 service 意义不大 |
| `utils/validators.py` | 校验工具函数，被 routes 和 services 共用，位置合理 |
| `utils/database.py` | 通用数据库工具（`get_or_create`、`session_scope`），仍然有效 |
| `models.py` | 数据模型定义，无需改动 |

---

## 3. 各层详细说明

### 3.1 Services 层（4个文件全部从空→实现）

#### `timer_service.py` — 计时核心

```
start_timer(title, tag_ids, is_pomodoro)
  → 检查是否已有进行中的计时
  → 创建 TimerRecord
  → 写入 OperationLog
  → 更新全局计时状态
  → 返回 (success, response_dict, http_status)

pause_timer() / resume_timer() / end_timer()
  → 同理，各自处理状态转换和日志

get_current_timer()
  → 查询当前记录 + 实时计算已用时间（减去暂停累计）
  → 状态不一致时自动重置

reset_current_timer()
  → 内部辅助函数，重置全局状态
```

全局状态 `current_timer` 字典保留在 service 层（运行时内存），不暴露给 routes。

#### `stats_service.py` — 统计聚合

```
get_today_stats()
  → 查询今日已完成记录
  → 计算 4 个概览卡片数值（总时长/任务数/最长连续/当前任务）
  → 生成 24 小时时段分布（柱状图数据）
  → 生成 Top5 任务占比（饼图数据）

get_trend_stats(days)
  → 按天遍历 N 天，每天汇总专注分钟数
  → 返回 {date, minutes} 列表（折线图数据）

get_task_ranking(start_date, end_date, limit)
  → 按标题聚合所有完成记录的总时长
  → 排序取 Top N，计算百分比
  → 返回排行榜
```

#### `backup_service.py` — 数据备份

```
create_backup()
  → 复制 focus_timer.db 到 backup 目录
  → 文件名带时间戳（focus_timer_backup_20260605_143000.db）

cleanup_old_backups(retention_days=30)
  → 遍历备份目录，删除超过保留期的文件

get_backup_list()
  → 列出所有备份文件（大小、时间）

auto_backup()
  → 先清理 → 再备份（供定时任务调用）
```

#### `sound_service.py` — 音效管理

```
validate_sound_file(file)
  → 检查扩展名（mp3/wav）、文件名非空

save_sound_file(file)
  → 校验 → 检查大小（≤5MB）→ 生成唯一文件名 → 保存到 static/sounds/

get_sound_path(event_type, custom_path)
  → 有自定义音效用自定义，没有则返回默认路径

get_default_sounds_list()
  → 列出 6 种事件的默认音效文件状态
```

### 3.2 Routes 层变化对比

#### `timer.py` 瘦身前后

```
重构前: start() 方法 54 行（校验 + 创建记录 + 写日志 + 状态管理 + 返回）
重构后: _start() 方法 10 行（校验参数 → 调 start_timer() → 返回结果）
```

代码量减少 **76%**（268行 → 65行）。

#### `stats.py` 瘦身前后

```
重构前: TodayStatsAPI.get() 56 行（SQL 查询 + 循环聚合 + 数据组装）
重构后: TodayStatsAPI.get() 3 行（调 get_today_stats() → 返回）
```

代码量减少 **74%**（172行 → 45行）。

### 3.3 新增路由（2条）

| 方法 | 路径 | 功能 | 对应的 req.md |
|------|------|------|---------------|
| GET | `/api/backup` | 手动触发一次备份 | FR-013 |
| GET | `/api/backup/list` | 获取备份文件列表 | FR-013 设置页查看 |
| DELETE | `/api/templates/<id>` | 删除指定模板 | FR-020（之前是坏的） |

---

## 4. 架构对比图

```
┌────────────────── 重构前 ──────────────────┐
│                                              │
│  前端 ──HTTP──→ routes/timer.py              │
│                │  ├── request.get_json()      │
│                │  ├── validate_title()        │
│                │  ├── TimerRecord(...)        │
│                │  ├── db.session.add()        │
│                │  ├── OperationLog(...)       │
│                │  ├── db.session.commit()     │
│                │  └── return jsonify(...)     │
│                ↓                              │
│              models.py / SQLite               │
│                                              │
│  services/ 目录: 4个空文件                    │
└──────────────────────────────────────────────┘

┌────────────────── 重构后 ──────────────────┐
│                                              │
│  前端 ──HTTP──→ routes/timer.py              │
│                │  ├── validate_title()  ←校验  │
│                │  └── start_timer(...)  ←转发  │
│                     ↓                        │
│              services/timer_service.py        │
│                │  ├── TimerRecord(...)        │
│                │  ├── db.session.add()        │
│                │  ├── OperationLog(...)       │
│                │  └── db.session.commit()     │
│                     ↓                        │
│              models.py / SQLite               │
│                                              │
│  services/ 目录: 4个实现文件，共 ~580 行      │
└──────────────────────────────────────────────┘
```

---

## 5. 验证结果

- ✅ Flask 应用正常启动，无 import 错误
- ✅ 所有原有路由保持兼容（路径、参数、响应格式不变）
- ✅ 新增 3 条 API 路由（备份×2 + 模板删除×1）
- ✅ 模板 DELETE 接口从「返回404」修复为正常工作

---

## 6. 下一步建议

按优先级排列：

| 优先级 | 任务 | 说明 |
|--------|------|------|
| **P0** | 搭建前端 Vue 3 项目 | `npm create vite@latest frontend -- --template vue`，配置 `vite.config.js` 代理到 Flask 5000 端口 |
| **P0** | 实现首页计时面板 | `HomeView.vue` — 大计时器 + 开始/暂停/结束按钮 + 当前任务标题 |
| **P1** | 前后端联调计时功能 | 前端调 `/api/timer/start` 等接口，验证完整链路 |
| **P1** | 实现今日概览卡片 | 调 `/api/stats/today` 展示 4 个统计卡片 |
| **P2** | 继续抽 service 层 | `records.py` 和 `tags.py` 也可考虑抽出 service（非紧急） |
| **P2** | 写单元测试 | 现在 service 层可以独立测试了，`backend/tests/` 目录已规划 |
| **P3** | 默认音效文件 | 准备 6 个 .mp3 文件放到 `backend/static/sounds/` |

---

## 7. 给新加入开发者的说明

在重构后的架构中，添加一个新功能的正确姿势：

1. **在 `models.py`** 定义/确认数据表
2. **在 `services/xxx_service.py`** 写业务逻辑函数，返回 `(result_dict, http_status)`
3. **在 `routes/xxx.py`** 写 Resource 类，只做参数解析 + 调 service + return
4. **在 `__init__.py`** 的 `register_api_routes()` 注册新路由

**原则**: Routes 不知道数据库怎么操作，Services 不知道 HTTP 请求长什么样。
