"""
停车场管理系统启动文件
"""
import os
from app import create_app
from app.models import db, User, ParkingSpot, Vehicle, Payment, Log

# 根据环境变量创建应用实例
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    """定义flask shell上下文"""
    return dict(db=db, User=User, ParkingSpot=ParkingSpot,
                Vehicle=Vehicle, Payment=Payment, Log=Log)


@app.cli.command('init-db')
def init_db():
    """初始化数据库"""
    from app.models import User
    from werkzeug.security import generate_password_hash
    
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
    from app.models import ParkingSpot
    from config import Config
    
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


if __name__ == '__main__':
    app.run(debug=True)
