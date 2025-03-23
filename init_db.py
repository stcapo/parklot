"""
数据库初始化脚本
"""
import os
from app import create_app, db
from app.models import User, ParkingSpot
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
        is_admin=True
    )
    
    # 创建工作人员用户
    staff = User(
        username='staff',
        email='staff@example.com',
        password_hash=generate_password_hash('staff123'),
        is_admin=False
    )
    
    db.session.add(admin)
    db.session.add(staff)
    
    # 初始化停车位
    # 初始化小汽车停车位
    for i in range(1, Config.MAX_CAR_SPOTS + 1):
        spot = ParkingSpot(
            spot_number=f'C-{i:03d}',
            spot_type='car',
            is_available=True
        )
        db.session.add(spot)
    
    # 初始化摩托车停车位
    for i in range(1, Config.MAX_MOTORCYCLE_SPOTS + 1):
        spot = ParkingSpot(
            spot_number=f'M-{i:03d}',
            spot_type='motorcycle',
            is_available=True
        )
        db.session.add(spot)
    
    # 初始化卡车停车位
    for i in range(1, Config.MAX_TRUCK_SPOTS + 1):
        spot = ParkingSpot(
            spot_number=f'T-{i:03d}',
            spot_type='truck',
            is_available=True
        )
        db.session.add(spot)
    
    db.session.commit()
    print('数据库初始化完成!')
