"""
统计数据 API 路由层
职责：接收前端请求 → 调 service 层 → 返回 JSON
不直接操作数据库，所有聚合逻辑在 services/stats_service.py
"""

from flask import request
from flask_restful import Resource

from backend.app.services.stats_service import (
    get_today_stats, get_trend_stats, get_task_ranking
)


class TodayStatsAPI(Resource):
    """今日统计数据（首页4个概览卡片 + 图表数据）"""

    def get(self):
        response, status = get_today_stats()
        return response, status


class TrendStatsAPI(Resource):
    """趋势数据（折线图）"""

    def get(self):
        # 路由层只做参数解析和校验
        range_days = request.args.get('range', '7')
        try:
            days = int(range_days)
        except ValueError:
            days = 7

        response, status = get_trend_stats(days=days)
        return response, status


class TaskRankingAPI(Resource):
    """任务统计排名（Top N）"""

    def get(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 10))

        response, status = get_task_ranking(
            start_date_str=start_date,
            end_date_str=end_date,
            limit=limit
        )
        return response, status
