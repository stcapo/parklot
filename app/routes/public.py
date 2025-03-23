"""
公共路由
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

public = Blueprint('public', __name__)


@public.route('/')
def index():
    """首页"""
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('staff.dashboard'))
    
    return render_template('index.html')


@public.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')


@public.route('/contact')
def contact():
    """联系我们"""
    return render_template('contact.html')
