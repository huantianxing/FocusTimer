from backend.app import db
from contextlib import contextmanager


@contextmanager
def session_scope():
    """提供数据库会话上下文管理器，安全操作数据库，自动提交 / 回滚 / 关闭；查不到就创建，查到就返回（超级常用）"""
    try:
        yield db.session # 给你一个数据库会话
        db.session.commit() # 成功 → 自动提交
    except Exception:
        db.session.rollback() # 失败 → 自动回滚（撤销操作）
        raise
    finally:
        db.session.close() # 最后 → 自动关闭





def get_or_create(model, defaults=None, **kwargs):
    """获取或创建记录"""
    # 1. 先按条件查询

    instance = model.query.filter_by(**kwargs).first()
    if instance:
        # 2. 查到了 → 返回，不创建
        return instance, False
    else:
        # 3. 没查到 → 创建一个新的
        params = {k: v for k, v in kwargs.items()}
        if defaults:
            params.update(defaults)
        instance = model(**params)
        db.session.add(instance)
        db.session.commit()
        return instance, True
"""
有就返回，没有就创建，自动处理！
举个例子（你马上懂）
你想获取标签 “学习”，不存在就创建：
python
运行
tag, created = get_or_create(Tag, name="学习")
如果表里有 “学习” → 返回它，created=False
如果没有 → 自动创建，created=True
不用你写 if 查询 + 手动创建！
"""

