"""
日志模型
"""
from datetime import datetime
from app import db


class Log(db.Model):
    """系统操作日志模型"""
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(50), nullable=False)  # 'login', 'logout', 'vehicle_entry', 'vehicle_exit', 'payment', etc.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    
    @classmethod
    def log_action(cls, user_id, action, details=None, ip_address=None):
        """记录用户操作"""
        log = cls(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=ip_address
        )
        db.session.add(log)
        db.session.commit()
        return log
    
    @classmethod
    def get_recent_logs(cls, limit=100):
        """获取最近的日志记录"""
        return cls.query.order_by(cls.timestamp.desc()).limit(limit).all()
    
    def __repr__(self):
        timestamp_str = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'<Log {self.action} by User {self.user_id} at {timestamp_str}>'
