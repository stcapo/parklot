"""
模型单元测试
"""
import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Vehicle, ParkingSpot, Payment


class ModelsTestCase(unittest.TestCase):
    """测试数据库模型"""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # 创建测试用户
        self.admin = User(
            username='testadmin',
            email='testadmin@example.com',
            password='password',
            is_admin=True
        )
        
        self.staff = User(
            username='teststaff',
            email='teststaff@example.com',
            password='password',
            is_admin=False
        )
        
        # 创建测试停车位
        self.car_spot = ParkingSpot(
            spot_number='C-001',
            spot_type='car',
            is_available=True
        )
        
        db.session.add_all([self.admin, self.staff, self.car_spot])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password_hashing(self):
        """测试用户密码哈希"""
        user = User(username='test', password='cat')
        self.assertTrue(user.password_hash is not None)
        self.assertTrue(user.verify_password('cat'))
        self.assertFalse(user.verify_password('dog'))

    def test_user_roles(self):
        """测试用户角色"""
        self.assertTrue(self.admin.is_admin)
        self.assertFalse(self.staff.is_admin)

    def test_parking_spot_availability(self):
        """测试停车位可用性"""
        self.assertTrue(self.car_spot.is_available)
        
        # 创建车辆并占用停车位
        vehicle = Vehicle(
            plate_number='京A12345',
            vehicle_type='car',
            parking_spot_id=self.car_spot.id
        )
        self.car_spot.is_available = False
        
        db.session.add(vehicle)
        db.session.commit()
        
        self.assertFalse(self.car_spot.is_available)
        self.assertEqual(vehicle.parking_spot_id, self.car_spot.id)

    def test_vehicle_parking_duration(self):
        """测试车辆停车时长计算"""
        # 创建入场1小时的车辆
        entry_time = datetime.utcnow() - timedelta(hours=1)
        vehicle = Vehicle(
            plate_number='京B12345',
            vehicle_type='car',
            entry_time=entry_time
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        # 检查停车时长计算
        self.assertAlmostEqual(vehicle.parking_duration, 1.0, delta=0.1)
        
        # 设置出场时间并再次检查
        vehicle.exit_time = entry_time + timedelta(hours=2, minutes=30)
        db.session.commit()
        
        self.assertAlmostEqual(vehicle.parking_duration, 2.5, delta=0.1)

    def test_vehicle_fee_calculation(self):
        """测试车辆费用计算"""
        # 创建不同类型的车辆，停车2小时
        entry_time = datetime.utcnow() - timedelta(hours=2)
        
        car = Vehicle(
            plate_number='京C12345',
            vehicle_type='car',
            entry_time=entry_time
        )
        
        motorcycle = Vehicle(
            plate_number='京D12345',
            vehicle_type='motorcycle',
            entry_time=entry_time
        )
        
        truck = Vehicle(
            plate_number='京E12345',
            vehicle_type='truck',
            entry_time=entry_time
        )
        
        db.session.add_all([car, motorcycle, truck])
        db.session.commit()
        
        # 小汽车费率为10元/小时
        self.assertEqual(car.calculate_fee(), 20.0)
        
        # 摩托车费率为5元/小时
        self.assertEqual(motorcycle.calculate_fee(), 10.0)
        
        # 卡车费率为15元/小时
        self.assertEqual(truck.calculate_fee(), 30.0)


if __name__ == '__main__':
    unittest.main()
