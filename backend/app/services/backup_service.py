"""
数据库备份业务逻辑层
负责：手动备份、自动清理过期备份、获取备份列表
"""

import os
import shutil
import glob
from datetime import datetime, timedelta

from flask import current_app


def _get_backup_dir():
    """获取备份目录路径"""
    backup_dir = current_app.config.get('BACKUP_DIR', os.path.join(os.path.expanduser('~'), 'FocusTimer', 'backups'))
    os.makedirs(backup_dir, exist_ok=True)
    return backup_dir


def _get_db_path():
    """获取当前SQLite数据库文件路径"""
    instance_dir = current_app.config['INSTANCE_DIR']
    return os.path.join(instance_dir, 'focus_timer.db')


def create_backup():
    """
    手动创建数据库备份
    将当前 SQLite 数据库文件复制到备份目录，文件名带时间戳
    返回: (success: bool, result: dict)
    """
    try:
        db_path = _get_db_path()
        if not os.path.exists(db_path):
            return False, {'code': 500, 'message': '数据库文件不存在', 'data': None}

        backup_dir = _get_backup_dir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"focus_timer_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)

        shutil.copy2(db_path, backup_path)

        return True, {
            'code': 200,
            'message': '备份成功',
            'data': {
                'filename': backup_filename,
                'path': backup_path,
                'size_bytes': os.path.getsize(backup_path),
                'created_at': datetime.now().isoformat()
            }
        }
    except Exception as e:
        return False, {'code': 500, 'message': f'备份失败: {str(e)}', 'data': None}


def cleanup_old_backups(retention_days=None):
    """
    清理超过保留天数的旧备份
    参数: retention_days - 保留天数（默认从配置读取）
    返回: (deleted_count: int, deleted_files: list)
    """
    if retention_days is None:
        retention_days = current_app.config.get('BACKUP_RETENTION_DAYS', 30)

    backup_dir = _get_backup_dir()
    cutoff_date = datetime.now() - timedelta(days=retention_days)

    deleted_files = []
    pattern = os.path.join(backup_dir, 'focus_timer_backup_*.db')

    for filepath in glob.glob(pattern):
        try:
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_mtime < cutoff_date:
                os.remove(filepath)
                deleted_files.append(os.path.basename(filepath))
        except OSError:
            pass

    return len(deleted_files), deleted_files


def get_backup_list():
    """
    获取所有备份文件列表（按时间倒序）
    返回: list of dict
    """
    backup_dir = _get_backup_dir()
    pattern = os.path.join(backup_dir, 'focus_timer_backup_*.db')
    backups = []

    for filepath in sorted(glob.glob(pattern), reverse=True):
        try:
            stat = os.stat(filepath)
            backups.append({
                'filename': os.path.basename(filepath),
                'path': filepath,
                'size_bytes': stat.st_size,
                'created_at': datetime.fromtimestamp(stat.st_mtime).isoformat()
            })
        except OSError:
            continue

    return backups


def auto_backup():
    """
    自动备份（每日触发）
    先清理过期备份，再创建新备份
    返回: (success: bool, result: dict)
    """
    # 先清理旧备份
    deleted_count, _ = cleanup_old_backups()

    # 再创建新备份
    success, result = create_backup()

    if success:
        result['data']['deleted_old_backups'] = deleted_count

    return success, result
