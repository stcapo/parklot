"""
工作人员相关路由
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import Vehicle, ParkingSpot, Payment, Log
from app.utils.forms import VehicleEntryForm, VehicleExitForm, PaymentForm

staff = Blueprint('staff', __name__)


@staff.route('/')
@login_required
def dashboard():
    """工作人员控制面板"""
    # 获取停车场整体状况
    parking_summary = ParkingSpot.get_availability_summary()
    
    # 获取当前在场车辆数
    current_vehicles_count = Vehicle.query.filter_by(exit_time=None).count()
    
    # 获取今日已处理车辆数
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_vehicles_count = Vehicle.query.filter(Vehicle.entry_time >= today_start).count()
    
    # 获取最近入场的车辆
    recent_entries = Vehicle.query.filter_by(exit_time=None).order_by(Vehicle.entry_time.desc()).limit(5).all()
    
    return render_template(
        'staff/dashboard.html',
        parking_summary=parking_summary,
        current_vehicles_count=current_vehicles_count,
        today_vehicles_count=today_vehicles_count,
        recent_entries=recent_entries
    )


@staff.route('/vehicle-entry', methods=['GET', 'POST'])
@login_required
def vehicle_entry():
    """登记车辆入场"""
    form = VehicleEntryForm()
    
    # 动态获取可用车位
    if request.method == 'GET':
        vehicle_type = request.args.get('vehicle_type', 'car')
        available_spots = ParkingSpot.get_available_spots(vehicle_type)
        form.parking_spot_id.choices = [(spot.id, spot.spot_number) for spot in available_spots]
    
    if form.validate_on_submit():
        # 检查车牌是否已在停车场内
        existing_vehicle = Vehicle.query.filter_by(
            plate_number=form.plate_number.data.upper(),
            exit_time=None
        ).first()
        
        if existing_vehicle:
            flash(f'车牌为 {form.plate_number.data.upper()} 的车辆已在停车场内！', 'danger')
            return redirect(url_for('staff.vehicle_entry'))
        
        # 获取选择的停车位
        parking_spot = ParkingSpot.query.get(form.parking_spot_id.data)
        
        # 创建车辆记录
        vehicle = Vehicle(
            plate_number=form.plate_number.data.upper(),
            vehicle_type=form.vehicle_type.data,
            parking_spot_id=parking_spot.id,
            owner_name=form.owner_name.data,
            owner_phone=form.owner_phone.data
        )
        
        # 更新停车位状态
        parking_spot.is_available = False
        
        db.session.add(vehicle)
        db.session.commit()
        
        # 记录操作日志
        Log.log_action(
            user_id=current_user.id,
            action='vehicle_entry',
            details=f'车辆入场: {vehicle.plate_number}, 停车位: {parking_spot.spot_number}',
            ip_address=request.remote_addr
        )
        
        flash(f'车辆 {vehicle.plate_number} 已成功入场，停车位: {parking_spot.spot_number}', 'success')
        return redirect(url_for('staff.dashboard'))
    
    return render_template('staff/vehicle_entry.html', form=form)


@staff.route('/vehicle-exit', methods=['GET', 'POST'])
@login_required
def vehicle_exit():
    """处理车辆出场"""
    form = VehicleExitForm()
    
    if form.plate_number.data:
        # 查找在场车辆
        vehicle = Vehicle.query.filter_by(
            plate_number=form.plate_number.data.upper(),
            exit_time=None
        ).first()
        
        if vehicle:
            # 计算停车费用
            fee = vehicle.calculate_fee()
            return render_template(
                'staff/vehicle_exit.html',
                form=form,
                vehicle=vehicle,
                fee=fee
            )
        else:
            flash(f'没有找到车牌为 {form.plate_number.data.upper()} 的在场车辆！', 'danger')
    
    return render_template('staff/vehicle_exit.html', form=form)


@staff.route('/process-payment/<int:vehicle_id>', methods=['GET', 'POST'])
@login_required
def process_payment(vehicle_id):
    """处理支付"""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    # 检查车辆是否已出场
    if vehicle.exit_time is not None:
        flash('该车辆已经出场！', 'danger')
        return redirect(url_for('staff.dashboard'))
    
    form = PaymentForm()
    
    if form.validate_on_submit():
        # 创建支付记录
        payment = Payment(
            vehicle_id=vehicle.id,
            amount=vehicle.calculate_fee(),
            payment_method=form.payment_method.data,
            payment_status='completed',  # 直接标记为已完成，模拟支付成功
            receipt_number=f'RCP-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
            operator_id=current_user.id,
            invoice_required=form.invoice_required.data,
            invoice_title=form.invoice_title.data if form.invoice_required.data else None,
            invoice_tax_number=form.invoice_tax_number.data if form.invoice_required.data else None
        )
        
        # 更新车辆出场时间
        vehicle.exit_time = datetime.utcnow()
        
        # 释放停车位
        if vehicle.parking_spot:
            vehicle.parking_spot.is_available = True
        
        db.session.add(payment)
        db.session.commit()
        
        # 记录操作日志
        Log.log_action(
            user_id=current_user.id,
            action='vehicle_exit',
            details=f'车辆出场: {vehicle.plate_number}, 支付金额: {payment.amount}元',
            ip_address=request.remote_addr
        )
        
        flash(f'车辆 {vehicle.plate_number} 已成功出场，已收费: {payment.amount}元', 'success')
        
        # 跳转到打印收据页面
        return redirect(url_for('staff.print_receipt', payment_id=payment.id))
    
    # 预填充表单
    form.amount.data = vehicle.calculate_fee()
    
    return render_template(
        'staff/process_payment.html',
        form=form,
        vehicle=vehicle
    )


@staff.route('/vehicles')
@login_required
def vehicles():
    """车辆管理"""
    # 获取查询参数
    status = request.args.get('status', 'all')
    plate_search = request.args.get('plate', '')
    
    # 构建查询
    query = Vehicle.query
    
    if status == 'parked':
        query = query.filter_by(exit_time=None)
    elif status == 'exited':
        query = query.filter(Vehicle.exit_time != None)
    
    if plate_search:
        query = query.filter(Vehicle.plate_number.like(f'%{plate_search}%'))
    
    # 分页
    page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Vehicle.entry_time.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    vehicles = pagination.items
    
    return render_template(
        'staff/vehicles.html',
        vehicles=vehicles,
        pagination=pagination,
        status=status,
        plate_search=plate_search
    )


@staff.route('/payments')
@login_required
def payments():
    """支付记录"""
    # 分页
    page = request.args.get('page', 1, type=int)
    pagination = Payment.query.order_by(Payment.payment_time.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    payments = pagination.items
    
    # 计算总收入
    total_amount = sum(payment.amount for payment in payments)
    
    return render_template(
        'staff/payments.html',
        payments=payments,
        pagination=pagination,
        total_amount=total_amount
    )


@staff.route('/receipt/<int:payment_id>')
@login_required
def print_receipt(payment_id):
    """打印收据"""
    payment = Payment.query.get_or_404(payment_id)
    vehicle = payment.vehicle
    
    # 生成收据码
    from app.utils.helpers import generate_qr_code
    receipt_data = f"Receipt:{payment.receipt_number},Vehicle:{vehicle.plate_number},Time:{payment.payment_time.strftime('%Y-%m-%d %H:%M:%S')},Amount:{payment.amount}"
    qr_code = generate_qr_code(receipt_data)
    
    return render_template(
        'staff/receipt.html',
        payment=payment,
        vehicle=vehicle,
        qr_code=qr_code
    )
