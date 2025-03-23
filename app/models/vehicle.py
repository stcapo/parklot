"""
车辆模型
"""
from datetime import datetime
from app import db


class Vehicle(db.Model):
    """车辆模型，记录进出停车场的车辆信息"""
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    plate_number = db.Column(db.String(20), index=True, nullable=False)
    vehicle_type = db.Column(db.String(20), nullable=False)  # 'car', 'motorcycle', 'truck'
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    exit_time = db.Column(db.DateTime, nullable=True)
    
    # 关联停车位
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'))
    parking_spot = db.relationship('ParkingSpot', backref=db.backref('current_vehicle', uselist=False))
    
    # 关联支付记录
    payment = db.relationship('Payment', backref='vehicle', uselist=False)
    
    # 车主信息（可选）
    owner_name = db.Column(db.String(64), nullable=True)
    owner_phone = db.Column(db.String(20), nullable=True)
    
    @property
    def is_parked(self):
        """判断车辆是否仍在停车场内"""
        return self.exit_time is None
    
    @property
    def parking_duration(self):
        """计算停车时长（小时）"""
        if not self.exit_time:
            # 如果车辆仍在停车场，使用当前时间计算
            duration = datetime.utcnow() - self.entry_time
        else:
            duration = self.exit_time - self.entry_time
        
        # 转换为小时，向上取整到最小计费单位（如15分钟）
        hours = duration.total_seconds() / 3600
        
        # 向上取整到0.25小时（15分钟）
        return round(hours * 4) / 4
    
    def calculate_fee(self):
        """计算停车费用"""
        from config import Config
        
        duration = self.parking_duration
        
        # 根据车辆类型应用不同的费率
        if self.vehicle_type == 'car':
            rate = Config.CAR_RATE
        elif self.vehicle_type == 'motorcycle':
            rate = Config.MOTORCYCLE_RATE
        elif self.vehicle_type == 'truck':
            rate = Config.TRUCK_RATE
        else:
            rate = Config.CAR_RATE  # 默认使用小汽车费率
        
        return round(duration * rate, 2)
    
    def __repr__(self):
        status = "已停车" if self.is_parked else "已离开"
        return f'<Vehicle {self.plate_number} ({status})>'
