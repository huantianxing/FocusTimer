from flask import request
from flask_restful import Resource

from backend.app import db
from backend.app.models import Tag, TimerRecord
from backend.app.utils.validators import validate_tag_name, validate_color


class TagsAPI(Resource):
    """标签管理 - 获取所有标签、创建标签"""

    def get(self):
        """获取所有标签"""
        tags = Tag.query.order_by(Tag.id).all()

        # 统计每个标签的使用次数
        tag_usage = {}
        records = TimerRecord.query.filter(TimerRecord.tag_ids.isnot(None)).all()
        for record in records:
            if record.tag_ids:
                for tag_id in record.tag_ids.split(','):
                    tid = int(tag_id)
                    tag_usage[tid] = tag_usage.get(tid, 0) + 1

        result = []
        for tag in tags:
            tag_dict = tag.to_dict()
            tag_dict['usage_count'] = tag_usage.get(tag.id, 0)
            result.append(tag_dict)

        return {
            'code': 200,
            'message': 'ok',
            'data': result
        }, 200

    def post(self):
        """创建新标签"""
        data = request.get_json() if request.is_json else {}

        name = data.get('name', '').strip()
        color = data.get('color', '#409EFF')

        # 验证标签名
        valid, result = validate_tag_name(name)
        if not valid:
            return {'code': 400, 'message': result, 'data': None}, 400

        name = result

        # 验证颜色
        valid, result = validate_color(color)
        if not valid:
            return {'code': 400, 'message': result, 'data': None}, 400

        color = result

        # 检查是否已存在
        existing = Tag.query.filter_by(name=name).first()
        if existing:
            return {'code': 409, 'message': f'标签"{name}"已存在', 'data': None}, 409

        # 创建标签
        tag = Tag(name=name, color=color)
        db.session.add(tag)
        db.session.commit()

        return {
            'code': 200,
            'message': '创建成功',
            'data': tag.to_dict()
        }, 200


class TagDetailAPI(Resource):
    """单个标签的修改和删除"""

    def put(self, tag_id):
        """修改标签"""
        tag = db.session.get(Tag, tag_id)
        if not tag:
            return {'code': 404, 'message': '标签不存在', 'data': None}, 404

        data = request.get_json() if request.is_json else {}

        # 修改名称
        if 'name' in data:
            valid, result = validate_tag_name(data['name'])
            if not valid:
                return {'code': 400, 'message': result, 'data': None}, 400

            # 检查新名称是否已被其他标签使用
            existing = Tag.query.filter(Tag.name == result, Tag.id != tag_id).first()
            if existing:
                return {'code': 409, 'message': f'标签"{result}"已存在', 'data': None}, 409

            tag.name = result

        # 修改颜色
        if 'color' in data:
            valid, result = validate_color(data['color'])
            if not valid:
                return {'code': 400, 'message': result, 'data': None}, 400
            tag.color = result

        db.session.commit()

        return {
            'code': 200,
            'message': '修改成功',
            'data': tag.to_dict()
        }, 200

    def delete(self, tag_id):
        """删除标签"""
        tag = db.session.get(Tag, tag_id)
        if not tag:
            return {'code': 404, 'message': '标签不存在', 'data': None}, 404

        # 检查是否有任务使用此标签
        records = TimerRecord.query.filter(TimerRecord.tag_ids.contains(str(tag_id))).first()
        if records:
            return {
                'code': 422,
                'message': f'标签"{tag.name}"正在被任务使用，无法删除',
                'data': None
            }, 422

        db.session.delete(tag)
        db.session.commit()

        return {
            'code': 200,
            'message': '删除成功',
            'data': None
        }, 200