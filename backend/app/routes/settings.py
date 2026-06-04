from flask import request
from flask_restful import Resource
import os

from backend.app import db
from backend.app.models import UserSettings


class SettingsAPI(Resource):
    """用户设置 - 获取和更新"""

    def get(self):
        """获取用户设置"""
        settings = UserSettings.query.get(1)
        if not settings:
            # 如果不存在，创建默认设置
            settings = UserSettings(id=1)
            db.session.add(settings)
            db.session.commit()

        return {
            'code': 200,
            'message': 'ok',
            'data': settings.to_dict()
        }, 200

    def put(self):
        """更新用户设置"""
        settings = UserSettings.query.get(1)
        if not settings:
            settings = UserSettings(id=1)
            db.session.add(settings)

        data = request.get_json() if request.is_json else {}

        # 主题设置
        if 'theme_mode' in data:
            if data['theme_mode'] in ['system', 'light', 'dark']:
                settings.theme_mode = data['theme_mode']

        # 音效设置
        if 'sound_enabled' in data:
            settings.sound_enabled = 1 if data['sound_enabled'] else 0

        if 'sound_volume' in data:
            volume = int(data['sound_volume'])
            if 0 <= volume <= 100:
                settings.sound_volume = volume

        # 番茄钟设置
        if 'pomodoro_work_minutes' in data:
            minutes = int(data['pomodoro_work_minutes'])
            if 1 <= minutes <= 60:
                settings.pomodoro_work_minutes = minutes

        if 'pomodoro_short_break' in data:
            minutes = int(data['pomodoro_short_break'])
            if 1 <= minutes <= 30:
                settings.pomodoro_short_break = minutes

        if 'pomodoro_long_break' in data:
            minutes = int(data['pomodoro_long_break'])
            if 1 <= minutes <= 60:
                settings.pomodoro_long_break = minutes

        if 'pomodoro_cycles' in data:
            cycles = int(data['pomodoro_cycles'])
            if 1 <= cycles <= 8:
                settings.pomodoro_cycles = cycles

        # 备份设置
        if 'auto_backup_enabled' in data:
            settings.auto_backup_enabled = 1 if data['auto_backup_enabled'] else 0

        if 'backup_path' in data:
            settings.backup_path = data['backup_path']

        # 快捷键设置
        if 'global_hotkey_start' in data:
            settings.global_hotkey_start = data['global_hotkey_start']

        if 'global_hotkey_end' in data:
            settings.global_hotkey_end = data['global_hotkey_end']

        db.session.commit()

        return {
            'code': 200,
            'message': '设置已保存',
            'data': settings.to_dict()
        }, 200


class SoundUploadAPI(Resource):
    """音效上传"""

    def post(self):
        """上传自定义音效"""
        if 'file' not in request.files:
            return {'code': 400, 'message': '请选择要上传的文件', 'data': None}, 400

        file = request.files['file']
        if file.filename == '':
            return {'code': 400, 'message': '请选择要上传的文件', 'data': None}, 400

        # 检查文件类型
        allowed_extensions = {'mp3', 'wav'}
        file_ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else ''

        if file_ext not in allowed_extensions:
            return {
                'code': 400,
                'message': '不支持的文件格式，请上传 MP3 或 WAV 文件',
                'data': None
            }, 400

        # TODO: 保存文件到指定目录
        # 这里暂时返回成功，实际需要实现文件保存逻辑

        return {
            'code': 200,
            'message': '音效上传成功',
            'data': {
                'custom_sound_path': '/path/to/custom_sound.mp3'
            }
        }, 200