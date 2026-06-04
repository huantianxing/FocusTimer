from flask import request, jsonify, g
from flask_restful import Resource
from datetime import datetime
import json

from backend.app import db
from backend.app.models import TimerRecord, OperationLog
from backend.app.utils.validators import validate_title, require_json

# 全局当前计时状态（单用户模式，简单存储）
# 生产环境可以考虑使用缓存，这里用内存变量即可
# 正在计时吗？暂停到什么时候？暂停了多久？
current_timer = {
    'record_id': None,
    'is_running': False,
    'paused_at': None,
    'paused_seconds': 0
}


class TimerAPI(Resource):
    """计时器API - 支持开始、暂停、恢复、结束"""

    def post(self):
        """根据路径判断操作"""
        path = request.path

        if path.endswith('/start'):
            return self.start()
        elif path.endswith('/pause'):
            return self.pause()
        elif path.endswith('/resume'):
            return self.resume()
        elif path.endswith('/end'):
            return self.end()

        return {'code': 404, 'message': '未知操作', 'data': None}, 404

    def start(self):
        """开始计时"""
        global current_timer

        # 检查是否已有进行中的计时
        if current_timer['record_id'] is not None:
            # 检查数据库中是否真的有进行中的记录
            active_record = TimerRecord.query.filter_by(status=0).first()
            if active_record:
                return {
                    'code': 409,
                    'message': '已有进行中的计时任务，请先结束或暂停当前任务',
                    'data': {'record_id': active_record.id, 'title': active_record.title}
                }, 409

        # 获取请求参数
        data = request.get_json() if request.is_json else {}
        title = data.get('title', '').strip()
        tag_ids = data.get('tag_ids', [])
        is_pomodoro = data.get('is_pomodoro', 0)

        # 验证标题
        valid, result = validate_title(title)
        if not valid:
            return {'code': 400, 'message': result, 'data': None}, 400

        # 创建新记录
        now = datetime.now()
        record = TimerRecord(
            title=title,
            tag_ids=','.join(map(str, tag_ids)) if tag_ids else None,
            start_time=now,
            status=0,  # 进行中
            is_pomodoro=1 if is_pomodoro else 0,
            pomodoro_count=0
        )

        db.session.add(record)
        db.session.flush()  # 获取ID

        # 记录操作日志
        log = OperationLog(
            record_id=record.id,
            action='start',
            details=json.dumps({'title': title, 'tag_ids': tag_ids})
        )
        db.session.add(log)
        db.session.commit()

        # 更新全局状态
        current_timer['record_id'] = record.id
        current_timer['is_running'] = True
        current_timer['paused_at'] = None
        current_timer['paused_seconds'] = 0

        return {
            'code': 200,
            'message': '开始计时成功',
            'data': record.to_dict()
        }, 200

    def pause(self):
        """暂停计时"""
        global current_timer

        if current_timer['record_id'] is None:
            return {'code': 422, 'message': '没有进行中的计时任务', 'data': None}, 422

        record = TimerRecord.query.get(current_timer['record_id'])
        if not record or record.status != 0:
            return {'code': 422, 'message': '没有进行中的计时任务', 'data': None}, 422

        # 更新记录状态
        record.status = 2  # 已暂停
        db.session.add(record)

        # 记录操作日志
        log = OperationLog(
            record_id=record.id,
            action='pause',
            details=json.dumps({'paused_at': datetime.now().isoformat()})
        )
        db.session.add(log)
        db.session.commit()

        # 更新全局状态
        current_timer['is_running'] = False
        current_timer['paused_at'] = datetime.now()

        return {
            'code': 200,
            'message': '已暂停',
            'data': record.to_dict()
        }, 200

    def resume(self):
        """继续计时"""
        global current_timer

        if current_timer['record_id'] is None:
            return {'code': 422, 'message': '没有暂停的计时任务', 'data': None}, 422

        record = TimerRecord.query.get(current_timer['record_id'])
        if not record or record.status != 2:
            return {'code': 422, 'message': '没有暂停的计时任务', 'data': None}, 422

        # 计算暂停时长
        if current_timer['paused_at']:
            pause_duration = (datetime.now() - current_timer['paused_at']).seconds
            current_timer['paused_seconds'] += pause_duration

        # 恢复状态
        record.status = 0  # 进行中
        db.session.add(record)

        # 记录操作日志
        log = OperationLog(
            record_id=record.id,
            action='resume',
            details=json.dumps({'resumed_at': datetime.now().isoformat()})
        )
        db.session.add(log)
        db.session.commit()

        # 更新全局状态
        current_timer['is_running'] = True
        current_timer['paused_at'] = None

        return {
            'code': 200,
            'message': '已恢复计时',
            'data': record.to_dict()
        }, 200

    def end(self):
        """结束计时"""
        global current_timer

        if current_timer['record_id'] is None:
            return {'code': 422, 'message': '没有进行中的计时任务', 'data': None}, 422

        record = TimerRecord.query.get(current_timer['record_id'])
        if not record:
            current_timer = {'record_id': None, 'is_running': False, 'paused_at': None, 'paused_seconds': 0}
            return {'code': 422, 'message': '记录不存在', 'data': None}, 422

        now = datetime.now()

        # 计算实际时长（减去暂停时间）
        total_seconds = int((now - record.start_time).total_seconds()) - current_timer['paused_seconds']
        if total_seconds < 0:
            total_seconds = 0

        # 更新记录
        record.end_time = now
        record.duration_seconds = total_seconds
        record.status = 1  # 已完成
        record.updated_at = now

        db.session.add(record)

        # 记录操作日志
        log = OperationLog(
            record_id=record.id,
            action='end',
            details=json.dumps({
                'duration_seconds': total_seconds,
                'end_time': now.isoformat()
            })
        )
        db.session.add(log)
        db.session.commit()

        # 重置全局状态
        current_timer = {'record_id': None, 'is_running': False, 'paused_at': None, 'paused_seconds': 0}

        return {
            'code': 200,
            'message': '计时结束',
            'data': record.to_dict()
        }, 200





class CurrentTimerAPI(Resource):
    """获取当前进行中的计时任务"""

    def get(self):
        global current_timer

        if current_timer['record_id'] is None:
            return {
                'code': 200,
                'message': 'ok',
                'data': None
            }, 200

        record = TimerRecord.query.get(current_timer['record_id'])
        if not record or record.status not in [0, 2]:
            # 状态不一致，重置
            current_timer = {'record_id': None, 'is_running': False, 'paused_at': None, 'paused_seconds': 0}
            return {'code': 200, 'message': 'ok', 'data': None}, 200

        # 计算已用时间
        now = datetime.now()
        if record.status == 0:  # 进行中
            elapsed_seconds = int((now - record.start_time).total_seconds()) - current_timer['paused_seconds']
        elif record.status == 2:  # 已暂停
            if current_timer['paused_at']:
                elapsed_seconds = int((current_timer['paused_at'] - record.start_time).total_seconds()) - current_timer[
                    'paused_seconds']
            else:
                elapsed_seconds = record.duration_seconds
        else:
            elapsed_seconds = record.duration_seconds

        if elapsed_seconds < 0:
            elapsed_seconds = 0

        data = record.to_dict()
        data['elapsed_seconds'] = elapsed_seconds
        data['is_running'] = current_timer['is_running']

        return {
            'code': 200,
            'message': 'ok',
            'data': data
        }, 200