import os
import sys
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# 全局扩展实例
db = SQLAlchemy()


def get_frontend_dir():
    """
    返回前端构建产物目录的绝对路径。
    兼容两种场景：
    1. 开发/命令行运行：frontend/dist/ 在项目根目录
    2. PyInstaller 打包后：sys._MEIPASS 是临时解压目录
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后
        base = sys._MEIPASS
    else:
        # 正常 Python 运行
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    return os.path.join(base, 'frontend', 'dist')


def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__, instance_path=None)

    api = Api()

    # 加载配置
    from backend.config import config
    app.config.from_object(config.get(config_name, config['default']))

    # 确保目录存在
    os.makedirs(app.config['INSTANCE_DIR'], exist_ok=True)
    os.makedirs(app.config['BACKUP_DIR'], exist_ok=True)

    # 初始化扩展
    db.init_app(app)

    # CORS — 同时允许开发端口和生产端口
    CORS(app, origins=[
        'http://localhost:5173',
        'http://127.0.0.1:5173',
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'null',  # PyWebView 使用 null origin
    ])

    # 注册路由
    register_api_routes(api)
    api.init_app(app)
    register_error_handlers(app)

    # ----- 生产模式：托管前端静态文件 -----
    register_static_routes(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()
        init_default_data()

    return app


def register_static_routes(app):
    """
    注册前端静态文件路由。
    仅在「非开发模式」下生效——判断标准是前端 dist/ 目录是否存在。
    开发时 Vite 单独启动，不依赖 Flask 提供静态文件。
    """
    frontend_dir = get_frontend_dir()

    # 如果 dist 目录不存在（开发中），不注册静态路由
    if not os.path.isdir(frontend_dir):
        return

    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_dir, 'index.html')

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory(os.path.join(frontend_dir, 'assets'), filename)

    @app.route('/icons.svg')
    def serve_icons():
        return send_from_directory(frontend_dir, 'icons.svg')

    # SPA fallback — 所有非 API 路径返回 index.html
    @app.route('/<path:path>')
    def serve_spa(path):
        # 如果是 API 路径，交给 Flask-RESTful 处理
        if path.startswith('api/'):
            return jsonify({'code': 404, 'message': '接口不存在', 'data': None}), 404
        # 如果文件存在，直接返回
        file_path = os.path.join(frontend_dir, path)
        if os.path.isfile(file_path):
            return send_from_directory(frontend_dir, path)
        # 否则返回 index.html（Vue Router history 模式）
        return send_from_directory(frontend_dir, 'index.html')


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'code': 400, 'message': str(error), 'data': None}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'code': 404, 'message': '资源不存在', 'data': None}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'code': 500, 'message': '服务器内部错误', 'data': None}), 500


def register_api_routes(api):
    from backend.app.routes.timer import TimerAPI, CurrentTimerAPI
    from backend.app.routes.records import TodayRecordsAPI, RecordsAPI, RecordDetailAPI, RecordInvalidAPI
    from backend.app.routes.stats import TodayStatsAPI, TrendStatsAPI, TaskRankingAPI
    from backend.app.routes.tags import TagsAPI, TagDetailAPI
    from backend.app.routes.settings import SettingsAPI, SoundUploadAPI
    from backend.app.routes.templates import TemplatesAPI, TemplateDetailAPI
    from backend.app.routes.backup import BackupAPI, BackupListAPI

    api.add_resource(TimerAPI, '/api/timer/start', '/api/timer/pause', '/api/timer/resume', '/api/timer/end')
    api.add_resource(CurrentTimerAPI, '/api/timer/current')

    api.add_resource(TodayRecordsAPI, '/api/records/today')
    api.add_resource(RecordsAPI, '/api/records')
    api.add_resource(RecordDetailAPI, '/api/records/<int:record_id>')
    api.add_resource(RecordInvalidAPI, '/api/records/<int:record_id>/invalid')

    api.add_resource(TodayStatsAPI, '/api/stats/today')
    api.add_resource(TrendStatsAPI, '/api/stats/trend')
    api.add_resource(TaskRankingAPI, '/api/stats/tasks')

    api.add_resource(TagsAPI, '/api/tags')
    api.add_resource(TagDetailAPI, '/api/tags/<int:tag_id>')

    api.add_resource(SettingsAPI, '/api/settings')
    api.add_resource(SoundUploadAPI, '/api/settings/sound')

    api.add_resource(TemplatesAPI, '/api/templates')
    api.add_resource(TemplateDetailAPI, '/api/templates/<int:template_id>')

    api.add_resource(BackupAPI, '/api/backup')
    api.add_resource(BackupListAPI, '/api/backup/list')


def init_default_data():
    from backend.app.models import Tag, UserSettings

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

    settings = db.session.execute(db.select(UserSettings).filter_by(id=1)).scalar_one_or_none()
    if not settings:
        settings = UserSettings(id=1)
        db.session.add(settings)

    db.session.commit()
