"""
任务模板 API 路由层
职责：接收前端请求 → 校验参数 → 操作数据库 → 返回 JSON
"""

from flask import request
from flask_restful import Resource

from backend.app import db
from backend.app.models import TaskTemplate
from backend.app.utils.validators import validate_title


class TemplatesAPI(Resource):
    """任务模板列表 - 获取全部、创建新模板"""

    def get(self):
        """获取所有任务模板（按排序顺序）"""
        templates = TaskTemplate.query.order_by(TaskTemplate.sort_order, TaskTemplate.id).all()

        return {
            'code': 200,
            'message': 'ok',
            'data': [t.to_dict() for t in templates]
        }, 200

    def post(self):
        """创建新任务模板"""
        data = request.get_json() if request.is_json else {}

        title = data.get('title', '').strip()
        tag_ids = data.get('tag_ids', [])
        estimated_minutes = data.get('estimated_minutes')
        sort_order = data.get('sort_order', 0)

        # 校验标题
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


class TemplateDetailAPI(Resource):
    """单个模板操作 - 删除"""

    def delete(self, template_id):
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
