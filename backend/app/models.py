from datetime import datetime
from backend.app import db

"""  def to_dict(self):to_dict() 是模型的方法，把数据库数据 → 转成 JSON → 传给前端 Vue 前端才能显示你的记录、统计、设置。"""

class TimerRecord(db.Model):
    """任务记录主表。计时任务记录"""
    __tablename__ = 'timer_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    tag_ids = db.Column(db.String(255))  # 关联标签ID，逗号分隔
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration_seconds = db.Column(db.Integer, default=0)
    status = db.Column(db.SmallInteger, default=0)  # 0:进行中 1:已完成 2:已暂停 3:已中断 4:已标记无效
    is_pomodoro = db.Column(db.SmallInteger, default=0)
    pomodoro_count = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.SmallInteger, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'tag_ids': self.tag_ids.split(',') if self.tag_ids else [],
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'status': self.status,
            'is_pomodoro': self.is_pomodoro,
            'pomodoro_count': self.pomodoro_count,
        }

    def to_dict_with_tags(self, tag_map=None):
        """带标签详情的字典"""
        data = self.to_dict()
        if tag_map and self.tag_ids:
            tag_id_list = [int(tid) for tid in self.tag_ids.split(',') if tid]
            data['tags'] = [tag_map.get(tid) for tid in tag_id_list if tag_map.get(tid)]
        else:
            data['tags'] = []
        return data


class Tag(db.Model):
    """标签表"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    color = db.Column(db.String(7), default='#409EFF')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
        }


class DailyStats(db.Model):
    """每日统计缓存表 每日统计表"""
    __tablename__ = 'daily_stats'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stat_date = db.Column(db.Date, unique=True, nullable=False)
    total_seconds = db.Column(db.Integer, default=0)
    task_count = db.Column(db.Integer, default=0)
    top_task_title = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'stat_date': self.stat_date.isoformat(),
            'total_seconds': self.total_seconds,
            'task_count': self.task_count,
            'top_task_title': self.top_task_title,
        }


class OperationLog(db.Model):
    """操作日志表"""
    __tablename__ = 'operation_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    record_id = db.Column(db.Integer)
    action = db.Column(db.String(20), nullable=False)  # start/pause/resume/end/edit/mark_invalid
    action_time = db.Column(db.DateTime, default=datetime.now)
    details = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'record_id': self.record_id,
            'action': self.action,
            'action_time': self.action_time.isoformat(),
            'details': self.details,
        }


class UserSettings(db.Model):
    """用户设置表（单用户）"""
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, primary_key=True)
    theme_mode = db.Column(db.String(20), default='system')  # system/light/dark
    sound_enabled = db.Column(db.SmallInteger, default=1)
    sound_volume = db.Column(db.Integer, default=80)  # 0-100
    custom_sound_path = db.Column(db.String(255))
    pomodoro_work_minutes = db.Column(db.Integer, default=25)
    pomodoro_short_break = db.Column(db.Integer, default=5)
    pomodoro_long_break = db.Column(db.Integer, default=15)
    pomodoro_cycles = db.Column(db.Integer, default=4)
    auto_backup_enabled = db.Column(db.SmallInteger, default=1)
    backup_path = db.Column(db.String(255))
    global_hotkey_start = db.Column(db.String(50), default='Ctrl+Alt+S')
    global_hotkey_end = db.Column(db.String(50), default='Ctrl+Alt+E')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'theme_mode': self.theme_mode,
            'sound_enabled': bool(self.sound_enabled),
            'sound_volume': self.sound_volume,
            'custom_sound_path': self.custom_sound_path,
            'pomodoro_work_minutes': self.pomodoro_work_minutes,
            'pomodoro_short_break': self.pomodoro_short_break,
            'pomodoro_long_break': self.pomodoro_long_break,
            'pomodoro_cycles': self.pomodoro_cycles,
            'auto_backup_enabled': bool(self.auto_backup_enabled),
            'backup_path': self.backup_path,
            'global_hotkey_start': self.global_hotkey_start,
            'global_hotkey_end': self.global_hotkey_end,
        }


class TaskTemplate(db.Model):
    """任务模板表"""
    __tablename__ = 'task_templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    tag_ids = db.Column(db.String(255))
    estimated_minutes = db.Column(db.Integer)
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'tag_ids': self.tag_ids.split(',') if self.tag_ids else [],
            'estimated_minutes': self.estimated_minutes,
            'sort_order': self.sort_order,
        }