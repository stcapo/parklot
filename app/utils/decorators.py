"""
自定义装饰器
"""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """验证用户是否为管理员的装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('您没有访问该页面的权限', 'danger')
            return redirect(url_for('public.index'))
        return f(*args, **kwargs)
    return decorated_function
