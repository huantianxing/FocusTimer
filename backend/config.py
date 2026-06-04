import os
from datetime import timedelta


class Config:
    # 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # 数据库配置
    BASE_DIR = os.path.abspath(os.path.dirname(__file__)) #转为绝对路径
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(INSTANCE_DIR, "focus_timer.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 备份配置（学时，记录，数据 等）
    BACKUP_DIR = os.path.join(os.path.expanduser('~'), 'FocusTimer', 'backups')
    BACKUP_RETENTION_DAYS = 30

    # 计时默认配置
    DEFAULT_POMODORO_WORK = 25
    DEFAULT_POMODORO_SHORT_BREAK = 5
    DEFAULT_POMODORO_LONG_BREAK = 15
    DEFAULT_POMODORO_CYCLES = 4
    AUTO_PAUSE_THRESHOLD_MINUTES = 30

    # 音效配置
    SOUND_UPLOAD_MAX_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_SOUND_EXTENSIONS = {'mp3', 'wav'}

    # 分页默认值
    DEFAULT_PAGE_SIZE = 20

    # 任务标题限制
    TITLE_MIN_LENGTH = 1
    TITLE_MAX_LENGTH = 50


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}