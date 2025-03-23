"""
错误处理路由
"""
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(e):
    """404错误处理"""
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(403)
def forbidden(e):
    """403错误处理"""
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(500)
def internal_server_error(e):
    """500错误处理"""
    return render_template('errors/500.html'), 500
