"""
支付模型
"""
from datetime import datetime
from app import db


class Payment(db.Model):
    """支付模型，记录停车费用支付情况"""
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_time = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(20), nullable=False)  # 'cash', 'credit_card', 'wechat', 'alipay'
    payment_status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed', 'refunded'
    transaction_id = db.Column(db.String(100), nullable=True)
    receipt_number = db.Column(db.String(50), nullable=True)
    
    # 记录处理支付的工作人员
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    operator = db.relationship('User', backref='processed_payments')
    
    # 发票信息
    invoice_required = db.Column(db.Boolean, default=False)
    invoice_title = db.Column(db.String(100), nullable=True)
    invoice_tax_number = db.Column(db.String(50), nullable=True)
    
    @classmethod
    def get_daily_revenue(cls, date=None):
        """获取指定日期的收入统计"""
        if date is None:
            date = datetime.utcnow().date()
        
        # 计算日期范围
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())
        
        # 查询已完成支付的记录
        payments = cls.query.filter(
            cls.payment_status == 'completed',
            cls.payment_time >= start_datetime,
            cls.payment_time <= end_datetime
        ).all()
        
        # 按支付方式统计
        statistics = {
            'total': 0,
            'cash': 0,
            'credit_card': 0,
            'wechat': 0,
            'alipay': 0
        }
        
        for payment in payments:
            statistics['total'] += payment.amount
            if payment.payment_method in statistics:
                statistics[payment.payment_method] += payment.amount
        
        return statistics
    
    def __repr__(self):
        return f'<Payment {self.id} ¥{self.amount} ({self.payment_status})>'
