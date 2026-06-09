"""
统计数据业务逻辑层
负责：今日概览、趋势数据、任务排名等统计聚合计算
routes 层只需传参数进来，拿到结果返回给前端
"""

from datetime import datetime, timedelta
from collections import defaultdict

from backend.app import db
from backend.app.models import TimerRecord


def get_today_stats():
    """
    今日统计数据（首页4个概览卡片 + 柱状图 + 饼图数据）
    返回: dict
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    # 今日已完成的记录
    completed_records = TimerRecord.query.filter(
        TimerRecord.start_time >= today_start,
        TimerRecord.start_time <= today_end,
        TimerRecord.status == 1,
        TimerRecord.is_deleted == 0
    ).all()

    # 1. 总专注时长
    total_seconds = sum(r.duration_seconds for r in completed_records)
    total_hours = total_seconds / 3600

    # 2. 完成任务数
    task_count = len(completed_records)

    # 3. 最长连续专注时间
    max_continuous = max([r.duration_seconds for r in completed_records], default=0)
    max_continuous_minutes = max_continuous // 60

    # 4. 当前进行中的任务
    active_record = TimerRecord.query.filter_by(status=0, is_deleted=0).first()
    current_task = active_record.title if active_record else None

    # 5. 时段分布（每小时专注分钟数，给柱状图用）
    hourly_data = defaultdict(int)
    for record in completed_records:
        hour = record.start_time.hour
        hourly_data[hour] += record.duration_seconds // 60

    # 6. 任务占比（给饼图用，取Top5）
    task_data = defaultdict(int)
    for record in completed_records:
        task_data[record.title] += record.duration_seconds // 60

    top_tasks = sorted(task_data.items(), key=lambda x: x[1], reverse=True)[:5]
    pie_data = [{'name': name, 'value': minutes} for name, minutes in top_tasks]

    return {
        'code': 200,
        'message': 'ok',
        'data': {
            'total_seconds': total_seconds,
            'total_display': f"{int(total_hours)}小时{int(total_seconds % 3600 // 60)}分钟",
            'task_count': task_count,
            'max_continuous_minutes': max_continuous_minutes,
            'current_task': current_task,
            'hourly_data': [{'hour': h, 'minutes': hourly_data.get(h, 0)} for h in range(24)],
            'pie_data': pie_data
        }
    }, 200


def get_trend_stats(days=7):
    """
    趋势数据（折线图）— 最近N天每日总专注时长
    参数: days - 统计天数（默认7天）
    返回: (result_dict, http_status)
    """
    end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    start_date = end_date - timedelta(days=days - 1)

    daily_stats = defaultdict(int)

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        date_start = current_date.replace(hour=0, minute=0, second=0)
        date_end = current_date.replace(hour=23, minute=59, second=59)

        records = TimerRecord.query.filter(
            TimerRecord.start_time >= date_start,
            TimerRecord.start_time <= date_end,
            TimerRecord.status == 1,
            TimerRecord.is_deleted == 0
        ).all()

        total_seconds = sum(r.duration_seconds for r in records)
        daily_stats[current_date.strftime('%m/%d')] = total_seconds // 60

    trend_data = [{'date': date, 'minutes': minutes} for date, minutes in daily_stats.items()]

    return {
        'code': 200,
        'message': 'ok',
        'data': {
            'range_days': days,
            'trend': trend_data
        }
    }, 200


def get_task_ranking(start_date_str=None, end_date_str=None, limit=10):
    """
    任务统计排名（横向条形图，Top N）
    参数:
        start_date_str - 开始日期 ISO 格式字符串
        end_date_str   - 结束日期 ISO 格式字符串
        limit          - 返回前 N 名（默认10）
    返回: (result_dict, http_status)
    """
    query = TimerRecord.query.filter(
        TimerRecord.status == 1,
        TimerRecord.is_deleted == 0
    )

    # 日期范围筛选
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
            query = query.filter(TimerRecord.start_time >= start_date)
        except ValueError:
            pass

    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str)
            query = query.filter(TimerRecord.start_time <= end_date)
        except ValueError:
            pass

    records = query.all()

    # 按标题聚合统计
    task_stats = defaultdict(lambda: {'total_seconds': 0, 'count': 0})
    for record in records:
        task_stats[record.title]['total_seconds'] += record.duration_seconds
        task_stats[record.title]['count'] += 1

    # 计算总时长（给百分比用）
    total_seconds_all = sum(stats['total_seconds'] for stats in task_stats.values())

    # 排序取 Top N
    sorted_tasks = sorted(task_stats.items(), key=lambda x: x[1]['total_seconds'], reverse=True)[:limit]

    ranking = []
    for title, stats in sorted_tasks:
        hours = stats['total_seconds'] // 3600
        minutes = (stats['total_seconds'] % 3600) // 60
        percentage = (stats['total_seconds'] / total_seconds_all * 100) if total_seconds_all > 0 else 0

        ranking.append({
            'title': title,
            'total_seconds': stats['total_seconds'],
            'display_time': f"{hours}小时{minutes}分钟" if hours > 0 else f"{minutes}分钟",
            'count': stats['count'],
            'percentage': round(percentage, 1)
        })

    return {
        'code': 200,
        'message': 'ok',
        'data': ranking
    }, 200
