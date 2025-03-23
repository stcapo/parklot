"""
表单类
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

from .validators import validate_plate_number, validate_phone_number, validate_tax_number


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    """注册新用户表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password', message='两次输入的密码不一致')])
    name = StringField('姓名', validators=[Optional(), Length(1, 64)])
    phone = StringField('电话', validators=[Optional(), validate_phone_number])
    is_admin = BooleanField('管理员权限')
    submit = SubmitField('注册')


class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('当前密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[DataRequired(), Length(6, 20)])
    new_password2 = PasswordField('确认新密码', validators=[DataRequired(), EqualTo('new_password', message='两次输入的密码不一致')])
    submit = SubmitField('修改密码')


class UserForm(FlaskForm):
    """用户信息表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码 (留空表示不修改)', validators=[Optional(), Length(6, 20)])
    name = StringField('姓名', validators=[Optional(), Length(1, 64)])
    phone = StringField('电话', validators=[Optional(), validate_phone_number])
    is_admin = BooleanField('管理员权限')
    submit = SubmitField('保存')


class ParkingSpotForm(FlaskForm):
    """停车位信息表单"""
    spot_number = StringField('车位编号', validators=[DataRequired(), Length(1, 10)])
    spot_type = SelectField('车位类型', choices=[
        ('car', '小汽车'), 
        ('motorcycle', '摩托车'), 
        ('truck', '卡车')
    ], validators=[DataRequired()])
    is_disabled = BooleanField('残疾人专用')
    is_vip = BooleanField('VIP车位')
    location = StringField('位置', validators=[Optional(), Length(1, 50)])
    notes = TextAreaField('备注', validators=[Optional(), Length(0, 255)])
    submit = SubmitField('保存')


class VehicleEntryForm(FlaskForm):
    """车辆入场表单"""
    plate_number = StringField('车牌号', validators=[DataRequired(), validate_plate_number])
    vehicle_type = SelectField('车辆类型', choices=[
        ('car', '小汽车'), 
        ('motorcycle', '摩托车'), 
        ('truck', '卡车')
    ], validators=[DataRequired()])
    parking_spot_id = SelectField('停车位', coerce=int, validators=[DataRequired()])
    owner_name = StringField('车主姓名', validators=[Optional(), Length(1, 64)])
    owner_phone = StringField('车主电话', validators=[Optional(), validate_phone_number])
    submit = SubmitField('登记入场')


class VehicleExitForm(FlaskForm):
    """车辆出场表单"""
    plate_number = StringField('车牌号', validators=[DataRequired(), validate_plate_number])
    submit = SubmitField('查询')


class PaymentForm(FlaskForm):
    """支付处理表单"""
    amount = FloatField('金额', validators=[DataRequired()])
    payment_method = SelectField('支付方式', choices=[
        ('cash', '现金'), 
        ('credit_card', '信用卡'), 
        ('wechat', '微信支付'), 
        ('alipay', '支付宝')
    ], validators=[DataRequired()])
    invoice_required = BooleanField('需要发票')
    invoice_title = StringField('发票抬头', validators=[Optional(), Length(1, 100)])
    invoice_tax_number = StringField('税号', validators=[Optional(), validate_tax_number])
    submit = SubmitField('确认支付')
