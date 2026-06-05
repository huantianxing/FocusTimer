from flask import Flask, jsonify
from flask_cors import CORS # 跨域
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# 全局扩展实例，创建全局插件
db = SQLAlchemy()
api = Api()


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__, instance_path=None)

    # 加载配置
    from backend.config import config
    app.config.from_object(config.get(config_name, config['default']))

    # 确保instance目录存在
    import os
    os.makedirs(app.config['INSTANCE_DIR'], exist_ok=True)
    os.makedirs(app.config['BACKUP_DIR'], exist_ok=True)

    # 初始化扩展
    db.init_app(app)
    CORS(app, origins=['http://localhost:5173', 'http://127.0.0.1:5173'])
    api.init_app(app)

    # 注册错误处理器
    register_error_handlers(app)

    # 注册路由
    register_blueprints(app)
    register_api_routes()

    # 创建数据库表
    with app.app_context():
        db.create_all()
        init_default_data()

    return app


def register_error_handlers(app):
    """注册全局错误处理器"""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'code': 400, 'message': str(error), 'data': None}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'code': 404, 'message': '资源不存在', 'data': None}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'code': 500, 'message': '服务器内部错误', 'data': None}), 500


def register_blueprints(app):
    """注册蓝图（如果需要）"""
    # 目前使用Flask-RESTful，暂不需要蓝图
    pass


def register_api_routes():
    """注册API路由"""
    from backend.app.routes.timer import TimerAPI, CurrentTimerAPI
    from backend.app.routes.records import TodayRecordsAPI, RecordsAPI, RecordDetailAPI, RecordInvalidAPI
    from backend.app.routes.stats import TodayStatsAPI, TrendStatsAPI, TaskRankingAPI
    from backend.app.routes.tags import TagsAPI, TagDetailAPI
    from backend.app.routes.settings import SettingsAPI, SoundUploadAPI
    from backend.app.routes.templates import TemplatesAPI

    # 计时相关
    api.add_resource(TimerAPI, '/api/timer/start', '/api/timer/pause', '/api/timer/resume', '/api/timer/end')
    api.add_resource(CurrentTimerAPI, '/api/timer/current')

    # 记录相关
    api.add_resource(TodayRecordsAPI, '/api/records/today')
    api.add_resource(RecordsAPI, '/api/records')
    api.add_resource(RecordDetailAPI, '/api/records/<int:record_id>')
    api.add_resource(RecordInvalidAPI, '/api/records/<int:record_id>/invalid')

    # 统计相关
    api.add_resource(TodayStatsAPI, '/api/stats/today')
    api.add_resource(TrendStatsAPI, '/api/stats/trend')
    api.add_resource(TaskRankingAPI, '/api/stats/tasks')

    # 标签相关
    api.add_resource(TagsAPI, '/api/tags')
    api.add_resource(TagDetailAPI, '/api/tags/<int:tag_id>')

    # 设置相关
    api.add_resource(SettingsAPI, '/api/settings')
    api.add_resource(SoundUploadAPI, '/api/settings/sound')

    # 模板相关
    api.add_resource(TemplatesAPI, '/api/templates')


def init_default_data():
    """初始化默认数据（标签、设置等）"""
    from backend.app.models import Tag, UserSettings

    # 初始化默认标签
    default_tags = [
        {'name': '工作', 'color': '#409EFF'},
        {'name': '学习', 'color': '#67C23A'},
        {'name': '阅读', 'color': '#E6A23C'},
        {'name': '运动', 'color': '#F56C6C'},
        {'name': '休闲', 'color': '#909399'},
    ]

    for tag_data in default_tags:
        existing = db.session.execute(db.select(Tag).filter_by(name=tag_data['name'])).scalar_one_or_none()
        if not existing:
            tag = Tag(name=tag_data['name'], color=tag_data['color'])
            db.session.add(tag)

    # 初始化用户设置（单用户，id=1）
    settings = db.session.execute(db.select(UserSettings).filter_by(id=1)).scalar_one_or_none()
    if not settings:
        settings = UserSettings(id=1)
        db.session.add(settings)

    db.session.commit()