"""
数据库初始化脚本
"""
import os
import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, ParkingSpot, Vehicle, Payment, Log
from werkzeug.security import generate_password_hash
from config import Config

# 创建应用实例
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():
    # 删除并重新创建所有表
    db.drop_all()
    db.create_all()
    
    # 创建管理员用户
    admin = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin123'),
        is_admin=True,
        name='管理员',
        phone='13900000001'
    )
    
    # 创建工作人员用户
    staff = User(
        username='staff',
        email='staff@example.com',
        password_hash=generate_password_hash('staff123'),
        is_admin=False,
        name='张工',
        phone='13800000002'
    )
    
    # 创建更多的工作人员
    staff2 = User(
        username='staff2',
        email='staff2@example.com',
        password_hash=generate_password_hash('staff123'),
        is_admin=False,
        name='王工',
        phone='13800000003'
    )
    
    staff3 = User(
        username='staff3',
        email='staff3@example.com',
        password_hash=generate_password_hash('staff123'),
        is_admin=False,
        name='李工',
        phone='13800000004'
    )
    
    staff4 = User(
        username='manager',
        email='manager@example.com',
        password_hash=generate_password_hash('manager123'),
        is_admin=True,
        name='刘经理',
        phone='13900000005'
    )
    
    db.session.add_all([admin, staff, staff2, staff3, staff4])
    
    # 初始化停车位
    # 初始化小汽车停车位
    locations = ["1楼A区", "1楼B区", "2楼A区", "2楼B区", "3楼A区", "地下一层", "地下二层"]
    notes_templates = [
        "靠近电梯",
        "靠近出口",
        "宽敞车位",
        "角落位置",
        "靠近监控",
        "采光好",
        "靠近入口",
        ""  # 空备注
    ]
    
    for i in range(1, Config.MAX_CAR_SPOTS + 1):
        # 为部分车位设置特殊属性
        is_vip = (i % 10 == 0)  # 每10个设置一个VIP车位
        is_disabled = (i % 15 == 0)  # 每15个设置一个残疾人车位
        location = locations[i % len(locations)]
        notes = notes_templates[i % len(notes_templates)]
        
        spot = ParkingSpot(
            spot_number=f'C-{i:03d}',
            spot_type='car',
            is_available=True,
            is_vip=is_vip,
            is_disabled=is_disabled,
            location=location,
            notes=notes
        )
        db.session.add(spot)
    
    # 初始化摩托车停车位
    for i in range(1, Config.MAX_MOTORCYCLE_SPOTS + 1):
        location = locations[(i + 2) % len(locations)]
        notes = notes_templates[(i + 3) % len(notes_templates)]
        
        spot = ParkingSpot(
            spot_number=f'M-{i:03d}',
            spot_type='motorcycle',
            is_available=True,
            location=location,
            notes=notes
        )
        db.session.add(spot)
    
    # 初始化卡车停车位
    for i in range(1, Config.MAX_TRUCK_SPOTS + 1):
        location = "地下车库" if i <= 10 else "室外停车场"
        notes = "大型车位" if i % 2 == 0 else "标准卡车位" if i % 3 == 0 else ""
        
        spot = ParkingSpot(
            spot_number=f'T-{i:03d}',
            spot_type='truck',
            is_available=True,
            location=location,
            notes=notes
        )
        db.session.add(spot)
    
    db.session.commit()  # 提交停车位数据
    
    # 创建示例车辆数据
    # 当前时间
    now = datetime.utcnow()
    
    # 测试车牌
    car_plates = [
        '京A12345', '京B67890', '京C13579', '京D24680',
        '津A11111', '津B22222', '冀C33333', '京E44444',
        '京F55555', '京G66666', '京H77777', '京J88888',
        '粤A12345', '粤B54321', '苏C98765', '浙D45678',
        '沪E22334', '皖F34521', '鲁G55664', '闽H77889',
        '陕A45678', '豫B34567', '晋C23467', '渝D12345',
        '湘E98765', '鄂F76543', '赣G83721', '贵H27654'
    ]
    
    motorcycle_plates = [
        '京A1234D', '京B4567F', '京C7890H',
        '津D2345J', '冀E5678L', '京F9012N',
        '京G3456P', '京H7890R', '粤J1234T',
        '苏K5678V', '浙L9012X', '沪M3456Z'
    ]
    
    truck_plates = [
        '京A12345挂', '京B67890挂', '京C13579挂',
        '津D24680挂', '冀E11111挂', '京F22222挂',
        '京G33333挂', '京H44444挂', '粤J55555挂',
        '苏K66666挂', '浙L77777挂', '沪M88888挂'
    ]
    
    # 车主姓名
    first_names = ['张', '王', '李', '赵', '刘', '陈', '杨', '黄', '周', '吴', '郑', '孙', '马', '朱', '胡', '林', '郭', '何', '高', '罗']
    last_names = ['伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '洋', '艳', '勇', '军', '杰', '娟', '涛', '明', '超', '秀兰', '霞']
    
    company_names = ['中国移动', '中国联通', '中国电信', '阿里巴巴', '腾讯科技', '百度公司', '京东集团', '华为技术', '小米科技',
                     '滴滴出行', '字节跳动', '美团点评', '拼多多', '网易', '新浪', '搜狐', '奇虎360', '陆金所', '宝钢集团', '中石油']
    
    def generate_phone():
        """生成随机手机号"""
        prefixes = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '157', '158', '159', '182', '183', '187', '188', '189']
        return random.choice(prefixes) + ''.join(random.choice('0123456789') for _ in range(8))
    
    def generate_name():
        """生成随机姓名"""
        return random.choice(first_names) + random.choice(last_names)
    
    # 将所有车牌组合到一起
    all_plates = car_plates + motorcycle_plates + truck_plates
    
    # 生成车主信息
    owners_info = []
    for i in range(len(all_plates)):
        # 随机决定是个人还是公司
        is_company = (i % 10 == 0)
        
        if is_company:
            name = random.choice(company_names)
            phone = '010' + ''.join(random.choice('0123456789') for _ in range(8))
        else:
            name = generate_name()
            phone = generate_phone()
            
            # 有10%的概率没有登记车主信息
            if i % 10 == 9:
                name = ''
                phone = ''
            # 有10%的概率只有电话没有姓名
            elif i % 10 == 8:
                name = ''
            # 有10%的概率只有姓名没有电话
            elif i % 10 == 7:
                phone = ''
        
        owners_info.append((name, phone))
    
    # 用户ID列表
    staff_ids = [staff.id, staff2.id, staff3.id, staff4.id, admin.id]
    
    # 支付方式
    payment_methods = ['cash', 'credit_card', 'wechat', 'alipay']
    
    # 生成日志动作和详情
    log_actions = ['login', 'logout', 'vehicle_entry', 'vehicle_exit', 'register_user', 'edit_user', 'edit_parking_spot', 'change_password']
    log_details = {
        'login': ['用户登录成功', '登录系统', '成功登录系统'],
        'logout': ['用户登出', '安全退出系统', '登出系统'],
        'vehicle_entry': ['车辆入场登记', '登记车辆入场', '车辆进入停车场'],
        'vehicle_exit': ['车辆出场处理', '办理车辆出场', '车辆离开停车场'],
        'register_user': ['创建新用户', '添加系统用户', '注册新员工账号'],
        'edit_user': ['修改用户信息', '更新用户资料', '编辑员工信息'],
        'edit_parking_spot': ['修改停车位信息', '更新车位状态', '编辑车位属性'],
        'change_password': ['修改密码', '更新账户密码', '密码重置']
    }
    
    # 创建大量的在场车辆
    # 以当前时间为基准，创建30个在场车辆，入场时间从10分钟到12小时不等
    parked_vehicles = []
    for i in range(30):
        # 随机决定车辆类型及对应车牌
        vehicle_type_rand = random.random()
        if vehicle_type_rand < 0.7:  # 70%是小汽车
            vehicle_type = 'car'
            plate_number = random.choice(car_plates)
        elif vehicle_type_rand < 0.9:  # 20%是摩托车
            vehicle_type = 'motorcycle'
            plate_number = random.choice(motorcycle_plates)
        else:  # 10%是卡车
            vehicle_type = 'truck'
            plate_number = random.choice(truck_plates)
        
        # 入场时间从10分钟到12小时随机
        entry_time = now - timedelta(hours=random.uniform(0.15, 12))
        
        # 获取一个可用的对应类型停车位
        spot = ParkingSpot.query.filter_by(spot_type=vehicle_type, is_available=True).first()
        
        if spot:
            # 随机选择车主信息
            owner_idx = random.randint(0, len(owners_info) - 1)
            owner_name, owner_phone = owners_info[owner_idx]
            
            # 将停车位标记为已占用
            spot.is_available = False
            
            # 创建车辆记录
            vehicle = Vehicle(
                plate_number=plate_number,
                vehicle_type=vehicle_type,
                entry_time=entry_time,
                parking_spot_id=spot.id,
                owner_name=owner_name,
                owner_phone=owner_phone
            )
            db.session.add(vehicle)
            parked_vehicles.append(vehicle)
            
            # 创建入场日志
            user_id = random.choice(staff_ids)
            action = 'vehicle_entry'
            detail = f'车辆入场: {plate_number}, 停车位: {spot.spot_number}'
            log = Log(
                user_id=user_id,
                action=action,
                timestamp=entry_time,
                details=detail,
                ip_address=f'192.168.1.{random.randint(2, 254)}'
            )
            db.session.add(log)
    
    db.session.commit()  # 提交在场车辆数据
    
    # 创建已离场车辆和支付记录
    # 生成过去3天内的100条离场记录
    for i in range(100):
        # 随机决定车辆类型及对应车牌
        vehicle_type_rand = random.random()
        if vehicle_type_rand < 0.7:  # 70%是小汽车
            vehicle_type = 'car'
            plate_number = random.choice(car_plates)
        elif vehicle_type_rand < 0.9:  # 20%是摩托车
            vehicle_type = 'motorcycle'
            plate_number = random.choice(motorcycle_plates)
        else:  # 10%是卡车
            vehicle_type = 'truck'
            plate_number = random.choice(truck_plates)
        
        # 入场时间在过去3天内随机
        entry_time = now - timedelta(days=random.uniform(0, 3), hours=random.uniform(0, 23))
        
        # 停车时长从30分钟到8小时随机
        parking_duration = random.uniform(0.5, 8)
        exit_time = entry_time + timedelta(hours=parking_duration)
        
        # 如果出场时间晚于当前时间，跳过此记录
        if exit_time > now:
            continue
        
        # 随机选择车主信息
        owner_idx = random.randint(0, len(owners_info) - 1)
        owner_name, owner_phone = owners_info[owner_idx]
        
        # 创建车辆记录
        vehicle = Vehicle(
            plate_number=plate_number,
            vehicle_type=vehicle_type,
            entry_time=entry_time,
            exit_time=exit_time,
            owner_name=owner_name,
            owner_phone=owner_phone
        )
        db.session.add(vehicle)
        db.session.flush()  # 获取vehicle ID
        
        # 计算费用
        if vehicle_type == 'car':
            rate = Config.CAR_RATE
        elif vehicle_type == 'motorcycle':
            rate = Config.MOTORCYCLE_RATE
        else:
            rate = Config.TRUCK_RATE
        
        fee = round(parking_duration * rate, 2)
        
        # 创建支付记录
        payment_method = random.choice(payment_methods)
        user_id = random.choice(staff_ids)
        
        # 随机决定是否需要发票
        invoice_required = (random.random() < 0.3)  # 30%需要发票
        
        if invoice_required:
            if random.random() < 0.7:  # 70%是公司发票
                invoice_title = random.choice(company_names)
                invoice_tax_number = ''.join(random.choice('0123456789') for _ in range(15))
            else:  # 30%是个人发票
                invoice_title = generate_name()
                invoice_tax_number = None
        else:
            invoice_title = None
            invoice_tax_number = None
        
        payment = Payment(
            vehicle_id=vehicle.id,
            amount=fee,
            payment_time=exit_time,
            payment_method=payment_method,
            payment_status='completed',
            operator_id=user_id,
            receipt_number=f'RCP-{exit_time.strftime("%Y%m%d%H%M%S")}-{random.randint(100, 999)}',
            invoice_required=invoice_required,
            invoice_title=invoice_title,
            invoice_tax_number=invoice_tax_number
        )
        db.session.add(payment)
        
        # 创建出场日志
        action = 'vehicle_exit'
        detail = f'车辆出场: {plate_number}, 支付金额: {fee}元'
        log = Log(
            user_id=user_id,
            action=action,
            timestamp=exit_time,
            details=detail,
            ip_address=f'192.168.1.{random.randint(2, 254)}'
        )
        db.session.add(log)
    
    # 创建系统操作日志
    # 创建过去7天内的其他系统操作日志
    for i in range(200):
        # 随机选择用户ID
        user_id = random.choice(staff_ids)
        
        # 随机选择操作类型
        action = random.choice(log_actions)
        
        # 随机选择详情
        if action == 'vehicle_entry' or action == 'vehicle_exit':
            # 这些日志已经在车辆记录中创建，跳过
            continue
        else:
            detail = random.choice(log_details[action])
        
        # 随机生成时间戳
        log_time = now - timedelta(days=random.uniform(0, 7), hours=random.uniform(0, 23))
        
        # 创建日志
        log = Log(
            user_id=user_id,
            action=action,
            timestamp=log_time,
            details=detail,
            ip_address=f'192.168.1.{random.randint(2, 254)}'
        )
        db.session.add(log)
    
    # 提交所有数据
    db.session.commit()
    print('数据库初始化完成! 已生成大量测试数据。')
