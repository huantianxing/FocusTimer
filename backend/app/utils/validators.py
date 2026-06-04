from flask import request
from functools import wraps
import re


def validate_title(title):
    """验证任务标题"""
    if not title or not isinstance(title, str):
        return False, "任务标题不能为空"

    title = title.strip()
    if len(title) < 1 or len(title) > 50:
        return False, "任务标题长度必须在1-50个字符之间"

    return True, title.strip()


def validate_datetime(dt_str):
    """验证日期时间格式"""
    from datetime import datetime
    try:
        return True, datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return False, "日期时间格式无效"


def validate_tag_name(name):
    """验证标签名称"""
    if not name or not isinstance(name, str):
        return False, "标签名称不能为空"

    name = name.strip()
    if len(name) < 1 or len(name) > 10:
        return False, "标签名称长度必须在1-10个字符之间"

    if not re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9_\s]+$', name):
        return False, "标签名称只能包含中文、英文、数字、下划线和空格"

    return True, name.strip()


def validate_color(color):
    """验证颜色代码"""
    if not color:
        return True, '#409EFF'  # 默认颜色

    if not re.match(r'^#[0-9A-Fa-f]{6}$', color):
        return False, "颜色代码格式无效，应为 #RRGGBB"

    return True, color


def require_json(f):
    """装饰器：要求请求包含JSON数据"""

    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            from flask import jsonify
            return jsonify({'code': 400, 'message': '请求需要JSON格式', 'data': None}), 400
        return f(*args, **kwargs)

    return decorated

"""用在：
routes 接口层
services 业务层
保证数据干净、合法
"""