"""
计时器业务逻辑层
负责：开始/暂停/继续/结束计时的核心逻辑 + 运行时状态管理
routes 层只需调用这里的函数，不用直接操作数据库
"""

import json
from datetime import datetime

from backend.app import db
from backend.app.models import TimerRecord, OperationLog

# ============================================================
# 全局当前计时状态（单用户模式，运行时内存存储）
# 生产环境可考虑用 Redis 缓存，这里用内存变量
# ============================================================
current_timer = {
    'record_id': None,       # 当前计时记录的ID
    'is_running': False,     # 是否正在运行
    'paused_at': None,       # 暂停的时间点
    'paused_seconds': 0      # 累计暂停秒数
}


def reset_current_timer():
    """重置全局计时状态"""
    global current_timer
    current_timer = {
        'record_id': None,
        'is_running': False,
        'paused_at': None,
        'paused_seconds': 0
    }


def start_timer(title, tag_ids=None, is_pomodoro=False):
    """
    开始计时
    返回: (success: bool, result: dict, http_status: int)
    """
    global current_timer

    # 1. 检查是否已有进行中的计时
    if current_timer['record_id'] is not None:
        active_record = TimerRecord.query.filter_by(status=0).first()
        if active_record:
            return False, {
                'code': 409,
                'message': '已有进行中的计时任务，请先结束或暂停当前任务',
                'data': {'record_id': active_record.id, 'title': active_record.title}
            }, 409

    # 2. 创建新记录
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
    db.session.flush()  # 获取自增ID

    # 3. 记录操作日志
    log = OperationLog(
        record_id=record.id,
        action='start',
        details=json.dumps({'title': title, 'tag_ids': tag_ids or []})
    )
    db.session.add(log)
    db.session.commit()

    # 4. 更新全局状态
    current_timer['record_id'] = record.id
    current_timer['is_running'] = True
    current_timer['paused_at'] = None
    current_timer['paused_seconds'] = 0

    return True, {
        'code': 200,
        'message': '开始计时成功',
        'data': record.to_dict()
    }, 200


def pause_timer():
    """
    暂停计时
    返回: (success: bool, result: dict, http_status: int)
    """
    global current_timer

    # 1. 检查是否有进行中的计时
    if current_timer['record_id'] is None:
        return False, {'code': 422, 'message': '没有进行中的计时任务', 'data': None}, 422

    record = db.session.get(TimerRecord, current_timer['record_id'])
    if not record or record.status != 0:
        return False, {'code': 422, 'message': '没有进行中的计时任务', 'data': None}, 422

    # 2. 更新记录状态为"已暂停"
    record.status = 2
    db.session.add(record)

    # 3. 记录操作日志
    log = OperationLog(
        record_id=record.id,
        action='pause',
        details=json.dumps({'paused_at': datetime.now().isoformat()})
    )
    db.session.add(log)
    db.session.commit()

    # 4. 更新全局状态
    current_timer['is_running'] = False
    current_timer['paused_at'] = datetime.now()

    return True, {
        'code': 200,
        'message': '已暂停',
        'data': record.to_dict()
    }, 200


def resume_timer():
    """
    继续计时（从暂停状态恢复）
    返回: (success: bool, result: dict, http_status: int)
    """
    global current_timer

    # 1. 检查是否有暂停的计时
    if current_timer['record_id'] is None:
        return False, {'code': 422, 'message': '没有暂停的计时任务', 'data': None}, 422

    record = db.session.get(TimerRecord, current_timer['record_id'])
    if not record or record.status != 2:
        return False, {'code': 422, 'message': '没有暂停的计时任务', 'data': None}, 422

    # 2. 计算暂停时长
    if current_timer['paused_at']:
        pause_duration = (datetime.now() - current_timer['paused_at']).seconds
        current_timer['paused_seconds'] += pause_duration

    # 3. 恢复状态为"进行中"
    record.status = 0
    db.session.add(record)

    # 4. 记录操作日志
    log = OperationLog(
        record_id=record.id,
        action='resume',
        details=json.dumps({'resumed_at': datetime.now().isoformat()})
    )
    db.session.add(log)
    db.session.commit()

    # 5. 更新全局状态
    current_timer['is_running'] = True
    current_timer['paused_at'] = None

    return True, {
        'code': 200,
        'message': '已恢复计时',
        'data': record.to_dict()
    }, 200


def end_timer():
    """
    结束计时
    返回: (success: bool, result: dict, http_status: int)
    """
    global current_timer

    # 1. 检查是否有进行中的计时
    if current_timer['record_id'] is None:
        return False, {'code': 422, 'message': '没有进行中的计时任务', 'data': None}, 422

    record = db.session.get(TimerRecord, current_timer['record_id'])
    if not record:
        reset_current_timer()
        return False, {'code': 422, 'message': '记录不存在', 'data': None}, 422

    now = datetime.now()

    # 2. 计算实际时长（总时间 - 暂停时间）
    total_seconds = int((now - record.start_time).total_seconds()) - current_timer['paused_seconds']
    if total_seconds < 0:
        total_seconds = 0

    # 3. 更新记录
    record.end_time = now
    record.duration_seconds = total_seconds
    record.status = 1  # 已完成
    record.updated_at = now
    db.session.add(record)

    # 4. 记录操作日志
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

    # 5. 重置全局状态
    reset_current_timer()

    return True, {
        'code': 200,
        'message': '计时结束',
        'data': record.to_dict()
    }, 200


def get_current_timer():
    """
    获取当前进行中的计时任务（含实时已用时间）
    返回: (success: bool, result: dict, http_status: int)
    """
    global current_timer

    # 没有进行中的计时
    if current_timer['record_id'] is None:
        return True, {'code': 200, 'message': 'ok', 'data': None}, 200

    record = db.session.get(TimerRecord, current_timer['record_id'])

    # 状态不一致，重置
    if not record or record.status not in [0, 2]:
        reset_current_timer()
        return True, {'code': 200, 'message': 'ok', 'data': None}, 200

    # 计算已用时间
    now = datetime.now()
    if record.status == 0:  # 进行中
        elapsed_seconds = int((now - record.start_time).total_seconds()) - current_timer['paused_seconds']
    elif record.status == 2:  # 已暂停
        if current_timer['paused_at']:
            elapsed_seconds = int((current_timer['paused_at'] - record.start_time).total_seconds()) - current_timer['paused_seconds']
        else:
            elapsed_seconds = record.duration_seconds
    else:
        elapsed_seconds = record.duration_seconds

    if elapsed_seconds < 0:
        elapsed_seconds = 0

    data = record.to_dict()
    data['elapsed_seconds'] = elapsed_seconds
    data['is_running'] = current_timer['is_running']

    return True, {
        'code': 200,
        'message': 'ok',
        'data': data
    }, 200
