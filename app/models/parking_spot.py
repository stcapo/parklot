"""
停车位模型
"""
from app import db


class ParkingSpot(db.Model):
    """停车位模型，管理停车场内的停车位"""
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(10), unique=True, nullable=False)
    spot_type = db.Column(db.String(20), nullable=False)  # 'car', 'motorcycle', 'truck'
    is_available = db.Column(db.Boolean, default=True)
    is_reserved = db.Column(db.Boolean, default=False)
    is_disabled = db.Column(db.Boolean, default=False)  # 残疾人专用车位
    is_vip = db.Column(db.Boolean, default=False)  # VIP车位
    location = db.Column(db.String(50), nullable=True)  # 例如 '1楼', '2楼'
    notes = db.Column(db.String(255), nullable=True)
    
    @classmethod
    def get_available_spots(cls, vehicle_type):
        """获取指定类型的可用停车位"""
        return cls.query.filter_by(
            spot_type=vehicle_type,
            is_available=True
        ).all()
    
    @classmethod
    def get_availability_summary(cls):
        """获取各类型停车位的可用情况统计"""
        result = {}
        for spot_type in ['car', 'motorcycle', 'truck']:
            total = cls.query.filter_by(spot_type=spot_type).count()
            available = cls.query.filter_by(
                spot_type=spot_type,
                is_available=True
            ).count()
            
            result[spot_type] = {
                'total': total,
                'available': available,
                'occupied': total - available,
                'occupancy_rate': (total - available) / total if total > 0 else 0
            }
        
        return result
    
    def __repr__(self):
        status = "可用" if self.is_available else "已占用"
        return f'<ParkingSpot {self.spot_number} ({status})>'
