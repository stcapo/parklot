"""
自定义表单验证函数
"""
from wtforms.validators import ValidationError
import re


def validate_plate_number(form, field):
    """验证车牌号格式"""
    plate_number = field.data.upper()
    
    # 中国车牌号正则表达式
    pattern = r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼使领A-Z]{1}[A-Z]{1}[A-Z0-9]{4}[A-Z0-9挂学警港澳]{1}$'
    
    if not re.match(pattern, plate_number):
        raise ValidationError('请输入有效的车牌号码')


def validate_phone_number(form, field):
    """验证手机号格式"""
    if field.data:  # 可选字段，只在有值时验证
        pattern = r'^1[3-9]\d{9}$'  # 中国大陆手机号码
        
        if not re.match(pattern, field.data):
            raise ValidationError('请输入有效的手机号码')


def validate_tax_number(form, field):
    """验证税号格式"""
    if field.data:  # 可选字段，只在有值时验证
        # 统一社会信用代码或纳税人识别号
        pattern = r'^[0-9A-Z]{15,20}$'
        
        if not re.match(pattern, field.data):
            raise ValidationError('请输入有效的税号')
