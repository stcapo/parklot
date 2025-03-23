"""
停车场管理系统应用初始化
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config

# 创建扩展实例
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
bootstrap = Bootstrap()
moment = Moment()


def create_app(config_name):
    """
    应用工厂函数
    :param config_name: 配置名称
    :return: Flask应用实例
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化扩展
    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # 注册蓝图
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .routes.staff import staff as staff_blueprint
    app.register_blueprint(staff_blueprint, url_prefix='/staff')

    from .routes.public import public as public_blueprint
    app.register_blueprint(public_blueprint)

    from .routes.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    return app
