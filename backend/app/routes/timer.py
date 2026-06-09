"""
计时器 API 路由层
职责：接收前端请求 → 调 service 层 → 返回 JSON
不直接操作数据库，所有业务逻辑在 services/timer_service.py
"""

from flask import request
from flask_restful import Resource

from backend.app.services.timer_service import (
    start_timer, pause_timer, resume_timer, end_timer, get_current_timer
)
from backend.app.utils.validators import validate_title


class TimerAPI(Resource):
    """计时器操作 - 开始、暂停、继续、结束"""

    def post(self):
        """根据请求路径分发到对应操作"""
        path = request.path

        if path.endswith('/start'):
            return self._start()
        elif path.endswith('/pause'):
            return self._pause()
        elif path.endswith('/resume'):
            return self._resume()
        elif path.endswith('/end'):
            return self._end()

        return {'code': 404, 'message': '未知操作', 'data': None}, 404

    def _start(self):
        """开始计时：校验参数 → 调 service"""
        data = request.get_json() if request.is_json else {}

        title = data.get('title', '').strip()
        tag_ids = data.get('tag_ids', [])
        is_pomodoro = data.get('is_pomodoro', False)

        # 路由层只做参数校验，业务逻辑全部交给 service
        valid, result = validate_title(title)
        if not valid:
            return {'code': 400, 'message': result, 'data': None}, 400

        success, response, status = start_timer(
            title=result,
            tag_ids=tag_ids,
            is_pomodoro=is_pomodoro
        )
        return response, status

    def _pause(self):
        """暂停计时"""
        success, response, status = pause_timer()
        return response, status

    def _resume(self):
        """继续计时"""
        success, response, status = resume_timer()
        return response, status

    def _end(self):
        """结束计时"""
        success, response, status = end_timer()
        return response, status


class CurrentTimerAPI(Resource):
    """获取当前进行中的计时任务"""

    def get(self):
        success, response, status = get_current_timer()
        return response, status
