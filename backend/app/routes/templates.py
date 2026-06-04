from flask import request
from flask_restful import Resource
import json

from backend.app import db
from backend.app.models import TaskTemplate
from backend.app.utils.validators import validate_title


class TemplatesAPI(Resource):
    """任务模板管理"""

    def get(self):
        """获取所有任务模板"""
        templates = TaskTemplate.query.order_by(TaskTemplate.sort_order, TaskTemplate.id).all()

        return {
            'code': 200,
            'message': 'ok',
            'data': [t.to_dict() for t in templates]
        }, 200

    def post(self):
        """创建任务模板"""
        data = request.get_json() if request.is_json else {}

        title = data.get('title', '').strip()
        tag_ids = data.get('tag_ids', [])
        estimated_minutes = data.get('estimated_minutes')
        sort_order = data.get('sort_order', 0)

        # 验证标题
        valid, result = validate_title(title)
        if not valid:
            return {'code': 400, 'message': result, 'data': None}, 400

        # 创建模板
        template = TaskTemplate(
            title=result,
            tag_ids=','.join(map(str, tag_ids)) if tag_ids else None,
            estimated_minutes=estimated_minutes,
            sort_order=sort_order
        )

        db.session.add(template)
        db.session.commit()

        return {
            'code': 200,
            'message': '模板创建成功',
            'data': template.to_dict()
        }, 200

    def put(self):
        """批量更新模板排序（可选）"""
        # 暂不实现批量更新
        return {'code': 404, 'message': 'Not Found', 'data': None}, 404

    def delete(self):
        """删除模板（需要ID）"""
        return {'code': 404, 'message': '请指定要删除的模板ID', 'data': None}, 404

    def delete_by_id(self, template_id):
        """删除指定模板"""
        template = TaskTemplate.query.get(template_id)
        if not template:
            return {'code': 404, 'message': '模板不存在', 'data': None}, 404

        db.session.delete(template)
        db.session.commit()

        return {
            'code': 200,
            'message': '删除成功',
            'data': None
        }, 200