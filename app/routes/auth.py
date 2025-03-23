"""
认证相关路由
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Log
from app.utils.forms import LoginForm, RegistrationForm, ChangePasswordForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            
            # 记录登录时间和日志
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            Log.log_action(
                user_id=user.id,
                action='login',
                details='用户登录成功',
                ip_address=request.remote_addr
            )
            
            # 根据用户类型跳转到不同的页面
            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('staff.dashboard'))
        
        flash('用户名或密码错误。', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """用户登出"""
    Log.log_action(
        user_id=current_user.id,
        action='logout',
        details='用户登出',
        ip_address=request.remote_addr
    )
    
    logout_user()
    flash('您已成功登出。', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    """注册新用户（仅供管理员使用）"""
    if not current_user.is_admin:
        flash('您没有权限注册新用户。', 'danger')
        return redirect(url_for('public.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            name=form.name.data,
            phone=form.phone.data,
            is_admin=form.is_admin.data
        )
        
        db.session.add(user)
        db.session.commit()
        
        Log.log_action(
            user_id=current_user.id,
            action='register_user',
            details=f'创建新用户: {user.username}',
            ip_address=request.remote_addr
        )
        
        flash('用户已成功注册。', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('auth/register.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """修改密码"""
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            
            Log.log_action(
                user_id=current_user.id,
                action='change_password',
                details='用户修改密码',
                ip_address=request.remote_addr
            )
            
            flash('您的密码已更新。', 'success')
            return redirect(url_for('public.index'))
        else:
            flash('当前密码错误。', 'danger')
    
    return render_template('auth/change_password.html', form=form)
