"""
管理员相关路由
"""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import User, Vehicle, ParkingSpot, Payment, Log
from app.utils.decorators import admin_required
from app.utils.forms import UserForm, ParkingSpotForm

admin = Blueprint('admin', __name__)


@admin.route('/')
@login_required
@admin_required
def dashboard():
    """管理员控制面板"""
    # 获取停车场整体状况
    parking_summary = ParkingSpot.get_availability_summary()
    
    # 获取今日收入
    today_revenue = Payment.get_daily_revenue()
    
    # 获取昨日收入
    yesterday = datetime.utcnow().date() - timedelta(days=1)
    yesterday_revenue = Payment.get_daily_revenue(yesterday)
    
    # 获取最近停车记录
    recent_vehicles = Vehicle.query.order_by(Vehicle.entry_time.desc()).limit(10).all()
    
    # 获取最近的系统日志
    recent_logs = Log.query.order_by(Log.timestamp.desc()).limit(10).all()
    
    return render_template(
        'admin/dashboard.html',
        parking_summary=parking_summary,
        today_revenue=today_revenue,
        yesterday_revenue=yesterday_revenue,
        recent_vehicles=recent_vehicles,
        recent_logs=recent_logs
    )


@admin.route('/users')
@login_required
@admin_required
def users():
    """用户管理"""
    all_users = User.query.all()
    return render_template('admin/users.html', users=all_users)


@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """编辑用户信息"""
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if form.validate_on_submit():
        if form.username.data != user.username and \
                User.query.filter_by(username=form.username.data).first():
            flash('该用户名已被使用。', 'danger')
            return render_template('admin/edit_user.html', form=form, user=user)
        
        if form.email.data != user.email and \
                User.query.filter_by(email=form.email.data).first():
            flash('该邮箱已被使用。', 'danger')
            return render_template('admin/edit_user.html', form=form, user=user)
        
        user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
        user.phone = form.phone.data
        user.is_admin = form.is_admin.data
        
        if form.password.data:
            user.password = form.password.data
        
        db.session.commit()
        
        Log.log_action(
            user_id=current_user.id,
            action='edit_user',
            details=f'编辑用户信息: {user.username}',
            ip_address=request.remote_addr
        )
        
        flash('用户信息已更新。', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)


@admin.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """删除用户"""
    user = User.query.get_or_404(user_id)
    
    # 不允许删除当前登录的用户
    if user.id == current_user.id:
        flash('不能删除您自己的账户。', 'danger')
        return redirect(url_for('admin.users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    Log.log_action(
        user_id=current_user.id,
        action='delete_user',
        details=f'删除用户: {username}',
        ip_address=request.remote_addr
    )
    
    flash(f'用户 {username} 已被删除。', 'success')
    return redirect(url_for('admin.users'))


@admin.route('/parking-spots')
@login_required
@admin_required
def parking_spots():
    """停车位管理"""
    spots = ParkingSpot.query.all()
    return render_template('admin/parking_spots.html', spots=spots)


@admin.route('/parking-spot/<int:spot_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_parking_spot(spot_id):
    """编辑停车位信息"""
    spot = ParkingSpot.query.get_or_404(spot_id)
    form = ParkingSpotForm(obj=spot)
    
    if form.validate_on_submit():
        if form.spot_number.data != spot.spot_number and \
                ParkingSpot.query.filter_by(spot_number=form.spot_number.data).first():
            flash('该车位编号已存在。', 'danger')
            return render_template('admin/edit_parking_spot.html', form=form, spot=spot)
        
        spot.spot_number = form.spot_number.data
        spot.spot_type = form.spot_type.data
        spot.is_disabled = form.is_disabled.data
        spot.is_vip = form.is_vip.data
        spot.location = form.location.data
        spot.notes = form.notes.data
        
        db.session.commit()
        
        Log.log_action(
            user_id=current_user.id,
            action='edit_parking_spot',
            details=f'编辑停车位信息: {spot.spot_number}',
            ip_address=request.remote_addr
        )
        
        flash('停车位信息已更新。', 'success')
        return redirect(url_for('admin.parking_spots'))
    
    return render_template('admin/edit_parking_spot.html', form=form, spot=spot)


@admin.route('/reports')
@login_required
@admin_required
def reports():
    """报表与统计"""
    # 获取日期范围
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = (datetime.utcnow() - timedelta(days=7)).date()
    
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        end_date = datetime.utcnow().date()
    
    # 按日汇总收入数据
    revenue_data = []
    current_date = start_date
    while current_date <= end_date:
        revenue = Payment.get_daily_revenue(current_date)
        revenue_data.append({
            'date': current_date.strftime('%Y-%m-%d'),
            'total': revenue['total'],
            'cash': revenue['cash'],
            'credit_card': revenue['credit_card'],
            'wechat': revenue['wechat'],
            'alipay': revenue['alipay']
        })
        current_date += timedelta(days=1)
    
    # 汇总各类型车辆数据
    vehicle_stats = {}
    for vehicle_type in ['car', 'motorcycle', 'truck']:
        count = Vehicle.query.filter(
            Vehicle.vehicle_type == vehicle_type,
            Vehicle.entry_time >= datetime.combine(start_date, datetime.min.time()),
            Vehicle.entry_time <= datetime.combine(end_date, datetime.max.time())
        ).count()
        
        vehicle_stats[vehicle_type] = count
    
    return render_template(
        'admin/reports.html',
        start_date=start_date,
        end_date=end_date,
        revenue_data=revenue_data,
        vehicle_stats=vehicle_stats
    )


@admin.route('/logs')
@login_required
@admin_required
def system_logs():
    """系统日志"""
    # 分页
    page = request.args.get('page', 1, type=int)
    pagination = Log.query.order_by(Log.timestamp.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    logs = pagination.items
    
    return render_template('admin/logs.html', logs=logs, pagination=pagination)


@admin.route('/settings')
@login_required
@admin_required
def settings():
    """系统设置"""
    # 这里可以添加系统配置项的管理
    return render_template('admin/settings.html')
