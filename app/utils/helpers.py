"""
辅助函数
"""
from datetime import datetime
import re
import qrcode
from io import BytesIO
import base64


def format_datetime(dt):
    """格式化日期时间显示"""
    if dt is None:
        return ''
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def format_currency(amount):
    """格式化金额显示"""
    return f'¥{amount:.2f}'


def validate_plate_number(plate_number):
    """验证车牌号格式"""
    # 中国车牌号正则表达式
    pattern = r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$'
    return re.match(pattern, plate_number) is not None


def calculate_parking_duration(entry_time, exit_time=None):
    """计算停车时长"""
    if exit_time is None:
        exit_time = datetime.utcnow()
    
    duration = exit_time - entry_time
    hours = duration.total_seconds() / 3600
    
    # 向上取整到0.25小时（15分钟）
    return round(hours * 4) / 4


def generate_qr_code(data, size=200):
    """生成二维码图像"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 将图像转换为Base64编码
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"


def generate_receipt_number():
    """生成唯一收据编号"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return f'RCP-{timestamp}'
