"""
数据库模型包初始化
"""
from app import db
from .user import User
from .vehicle import Vehicle
from .parking_spot import ParkingSpot
from .payment import Payment
from .log import Log

__all__ = ['db', 'User', 'Vehicle', 'ParkingSpot', 'Payment', 'Log']
