from flask import request
from flask_restful import Resource
from datetime import datetime, timedelta
import json

from backend.app import db
from backend.app.models import TimerRecord, OperationLog, Tag
from backend.app.utils.validators import validate_title, validate_datetime


class TodayRecordsAPI(Resource):
    """获取今日记录列表"""

    def get(self):
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

        records = TimerRecord.query.filter(
            TimerRecord.start_time >= today_start,
            TimerRecord.start_time <= today_end,
            TimerRecord.is_deleted == 0,
            TimerRecord.status.in_([1, 2, 3])  # 已完成、已暂停、已中断
        ).order_by(TimerRecord.start_time.desc()).all()

        # 获取所有标签
        tags = {tag.id: tag.to_dict() for tag in Tag.query.all()}

        # 按标题分组统计
        grouped = {}
        for record in records:
            title = record.title
            if title not in grouped:
                grouped[title] = {
                    'title': title,
                    'total_seconds': 0,
                    'records': []
                }
            grouped[title]['total_seconds'] += record.duration_seconds
            grouped[title]['records'].append(record.to_dict_with_tags(tags))

        # 转换为列表，按累计时长降序排序
        result = sorted(grouped.values(), key=lambda x: x['total_seconds'], reverse=True)

        # 格式化累计时长
        for group in result:
            hours = group['total_seconds'] // 3600
            minutes = (group['total_seconds'] % 3600) // 60
            group['total_display'] = f"{hours}小时{minutes}分钟" if hours > 0 else f"{minutes}分钟"

        return {
            'code': 200,
            'message': 'ok',
            'data': result
        }, 200


class RecordsAPI(Resource):
    """查询历史记录（分页+筛选）"""

    def get(self):
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        keyword = request.args.get('keyword', '').strip()
        tag_id = request.args.get('tag_id')
        page = int(request.args.get('page', 1))
        size = int(request.args.get('size', 20))

        # 构建查询
        query = TimerRecord.query.filter(
            TimerRecord.is_deleted == 0,
            TimerRecord.status.in_([1, 2, 3, 4])  # 已完成、已暂停、已中断、已标记无效
        )

        # 日期范围筛选
        if start_date:
            try:
                start = datetime.fromisoformat(start_date)
                query = query.filter(TimerRecord.start_time >= start)
            except ValueError:
                pass

        if end_date:
            try:
                end = datetime.fromisoformat(end_date)
                query = query.filter(TimerRecord.start_time <= end)
            except ValueError:
                pass

        # 关键词筛选
        if keyword:
            query = query.filter(TimerRecord.title.contains(keyword))

        # 标签筛选
        if tag_id:
            query = query.filter(TimerRecord.tag_ids.contains(str(tag_id)))

        # 分页
        total = query.count()
        records = query.order_by(TimerRecord.start_time.desc()).offset((page - 1) * size).limit(size).all()

        # 获取标签映射
        tags = {tag.id: tag.to_dict() for tag in Tag.query.all()}

        return {
            'code': 200,
            'message': 'ok',
            'data': {
                'total': total,
                'page': page,
                'size': size,
                'records': [r.to_dict_with_tags(tags) for r in records]
            }
        }, 200


class RecordDetailAPI(Resource):
    """修改记录"""

    def put(self, record_id):
        record = db.session.get(TimerRecord, record_id)
        if not record:
            return {'code': 404, 'message': '记录不存在', 'data': None}, 404

        data = request.get_json() if request.is_json else {}

        # 记录修改前的状态
        old_data = {
            'title': record.title,
            'tag_ids': record.tag_ids,
            'start_time': record.start_time.isoformat() if record.start_time else None,
            'end_time': record.end_time.isoformat() if record.end_time else None
        }

        changes = {}

        # 修改标题
        if 'title' in data:
            valid, result = validate_title(data['title'])
            if not valid:
                return {'code': 400, 'message': result, 'data': None}, 400
            record.title = result
            changes['title'] = {'old': old_data['title'], 'new': result}

        # 修改标签
        if 'tag_ids' in data:
            tag_ids = data['tag_ids']
            if tag_ids:
                record.tag_ids = ','.join(map(str, tag_ids))
            else:
                record.tag_ids = None
            changes['tag_ids'] = {'old': old_data['tag_ids'], 'new': record.tag_ids}

        # 修改开始时间
        if 'start_time' in data:
            valid, result = validate_datetime(data['start_time'])
            if not valid:
                return {'code': 400, 'message': result, 'data': None}, 400
            record.start_time = result
            changes['start_time'] = {'old': old_data['start_time'], 'new': result.isoformat()}

        # 修改结束时间
        if 'end_time' in data:
            valid, result = validate_datetime(data['end_time'])
            if not valid:
                return {'code': 400, 'message': result, 'data': None}, 400
            record.end_time = result
            # 重新计算时长
            if record.start_time and record.end_time:
                record.duration_seconds = int((record.end_time - record.start_time).total_seconds())
            changes['end_time'] = {'old': old_data['end_time'], 'new': result.isoformat()}

        record.updated_at = datetime.now()
        db.session.add(record)

        # 记录操作日志
        log = OperationLog(
            record_id=record.id,
            action='edit',
            details=json.dumps(changes, ensure_ascii=False)
        )
        db.session.add(log)
        db.session.commit()

        tags = {tag.id: tag.to_dict() for tag in Tag.query.all()}

        return {
            'code': 200,
            'message': '修改成功',
            'data': record.to_dict_with_tags(tags)
        }, 200


class RecordInvalidAPI(Resource):
    """标记记录为无效"""

    def post(self, record_id):
        record = db.session.get(TimerRecord, record_id)
        if not record:
            return {'code': 404, 'message': '记录不存在', 'data': None}, 404

        data = request.get_json() if request.is_json else {}
        reason = data.get('reason', '').strip()

        # 标记为无效
        record.status = 4  # 已标记无效
        record.updated_at = datetime.now()
        db.session.add(record)

        # 记录操作日志
        log = OperationLog(
            record_id=record.id,
            action='mark_invalid',
            details=json.dumps({'reason': reason}, ensure_ascii=False)
        )
        db.session.add(log)
        db.session.commit()

        tags = {tag.id: tag.to_dict() for tag in Tag.query.all()}

        return {
            'code': 200,
            'message': '已标记为无效',
            'data': record.to_dict_with_tags(tags)
        }, 200