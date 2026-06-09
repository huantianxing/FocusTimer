"""
音效文件管理业务逻辑层
负责：自定义音效上传、文件校验、路径管理
"""

import os
import uuid
from werkzeug.utils import secure_filename

from flask import current_app


# 允许的音效文件格式
ALLOWED_EXTENSIONS = {'mp3', 'wav'}
# 上传文件最大大小（5MB）
MAX_FILE_SIZE = 5 * 1024 * 1024

# 默认音效事件名称
SOUND_EVENTS = ['start', 'pause', 'end', 'break_start', 'break_end', 'goal_achieved']


def _get_sounds_dir():
    """获取音效文件存储目录"""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(current_app.root_path)), 'static', 'sounds')
    os.makedirs(static_dir, exist_ok=True)
    return static_dir


def validate_sound_file(file):
    """
    校验上传的音效文件
    返回: (is_valid: bool, error_message: str or None)
    """
    if not file or file.filename == '':
        return False, '请选择要上传的文件'

    # 检查扩展名
    file_ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f'不支持的文件格式 ".{file_ext}"，请上传 MP3 或 WAV 文件'

    return True, None


def save_sound_file(file):
    """
    保存上传的音效文件
    参数: file - Flask FileStorage 对象
    返回: (success: bool, result: dict)
    """
    # 1. 校验文件
    is_valid, error_msg = validate_sound_file(file)
    if not is_valid:
        return False, {'code': 400, 'message': error_msg, 'data': None}, 400

    # 2. 检查文件大小
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return False, {
            'code': 413,
            'message': f'文件过大（{file_size / 1024 / 1024:.1f}MB），最大允许 5MB',
            'data': None
        }, 413

    # 3. 生成唯一文件名并保存
    file_ext = file.filename.rsplit('.', 1)[-1].lower()
    unique_name = f"custom_{uuid.uuid4().hex[:8]}.{file_ext}"
    save_path = os.path.join(_get_sounds_dir(), unique_name)

    file.save(save_path)

    # 4. 返回相对路径（前端可直接通过 static 访问）
    relative_path = f"/static/sounds/{unique_name}"

    return True, {
        'code': 200,
        'message': '音效上传成功',
        'data': {
            'filename': unique_name,
            'custom_sound_path': relative_path,
            'size_bytes': file_size
        }
    }, 200


def get_sound_path(event_type, custom_path=None):
    """
    根据事件类型获取音效文件路径
    参数:
        event_type - 事件类型 (start/pause/end/break_start/break_end/goal_achieved)
        custom_path - 用户自定义路径（可选）
    返回: 音效文件的访问路径（前端用）
    """
    if custom_path and os.path.exists(os.path.join(current_app.root_path, '..', custom_path.lstrip('/'))):
        return custom_path

    # 返回默认音效路径
    return f"/static/sounds/{event_type}_default.mp3"


def get_default_sounds_list():
    """
    获取所有默认音效的列表
    返回: list of dict
    """
    sounds_dir = _get_sounds_dir()
    result = []

    for event in SOUND_EVENTS:
        filename = f"{event}_default.mp3"
        filepath = os.path.join(sounds_dir, filename)
        result.append({
            'event': event,
            'filename': filename,
            'exists': os.path.exists(filepath),
            'url': f"/static/sounds/{filename}"
        })

    return result
