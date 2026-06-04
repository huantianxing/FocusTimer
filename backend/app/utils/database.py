from backend.app import db
from contextlib import contextmanager


@contextmanager
def session_scope():
    """提供数据库会话上下文管理器"""
    try:
        yield db.session
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()


def get_or_create(model, defaults=None, **kwargs):
    """获取或创建记录"""
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {k: v for k, v in kwargs.items()}
        if defaults:
            params.update(defaults)
        instance = model(**params)
        db.session.add(instance)
        db.session.commit()
        return instance, True