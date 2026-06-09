"""
数据备份 API 路由层
职责：接收前端请求 → 调 service 层 → 返回 JSON
"""

from flask_restful import Resource

from backend.app.services.backup_service import create_backup, get_backup_list


class BackupAPI(Resource):
    """手动触发备份"""

    def get(self):
        """执行一次手动备份"""
        success, result = create_backup()
        if success:
            return result, 200
        return result, 500


class BackupListAPI(Resource):
    """获取备份文件列表"""

    def get(self):
        backups = get_backup_list()
        return {
            'code': 200,
            'message': 'ok',
            'data': {
                'total': len(backups),
                'backups': backups
            }
        }, 200
