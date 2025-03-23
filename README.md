# 停车场管理系统

一个功能丰富的停车场管理系统，使用Python 3.13.1、Flask框架和SQLite数据库。

## 功能特点

- 车辆入场与出场管理
- 停车位实时监控
- 多种支付方式支持
- 自动计费系统
- 财务报表和统计
- 用户权限管理
- 系统日志记录
- 发票生成

## 技术栈

- **后端**: Python 3.13.1, Flask 3.0.0
- **数据库**: SQLite, Flask-SQLAlchemy
- **前端**: HTML, CSS, JavaScript, Bootstrap 4
- **认证**: Flask-Login
- **表单处理**: Flask-WTF
- **Chart绘制**: Chart.js

## 系统需求

- Python 3.13.1或更高版本
- pip包管理工具
- 虚拟环境工具(可选，但推荐)

## 安装指南

### 1. 克隆或下载代码

```bash
git clone https://github.com/yourusername/parklot.git
cd parklot
```

或者下载ZIP压缩包并解压。

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 初始化数据库

```bash
# 设置Flask应用
# Windows:
set FLASK_APP=run.py
# macOS/Linux:
export FLASK_APP=run.py

# 初始化数据库
# 方法1 - 使用脚本
python init_db.py

# 方法2 - 使用Flask命令(如果环境变量设置正确)
flask init-db
```

这将创建数据库并添加默认的管理员用户(admin/admin123)和工作人员用户(staff/staff123)。

### 5. 运行应用

```bash
# 开发模式运行
flask run --debug

# 或者直接使用Python运行
python run.py
```

应用将在 http://127.0.0.1:5000/ 运行。

## 用户登录信息

系统预设了两个用户账号：

1. **管理员**:
   - 用户名: admin
   - 密码: admin123

2. **工作人员**:
   - 用户名: staff
   - 密码: staff123

## 项目结构

```
parklot/
├── app/                    # 应用主目录
│   ├── models/             # 数据库模型
│   ├── routes/             # 路由和视图
│   ├── static/             # 静态文件(CSS, JS, 图片)
│   ├── templates/          # HTML模板
│   ├── utils/              # 工具函数
│   └── __init__.py         # 应用初始化
├── instance/               # 实例文件夹(数据库)
├── migrations/             # 数据库迁移文件
├── tests/                  # 测试
├── config.py               # 配置文件
├── requirements.txt        # 依赖列表
└── run.py                  # 应用入口
```

## 系统使用指南

### 管理员功能

- 用户管理：创建、编辑和删除用户
- 停车位管理：配置停车位类型和状态
- 查看财务报表：收入统计和分析
- 系统设置：调整系统参数
- 查看系统日志：监控系统操作

### 工作人员功能

- 车辆入场登记：记录车辆信息和分配停车位
- 车辆出场处理：计算费用和处理支付
- 查看当前停车状态
- 查询车辆和支付记录
- 打印收据

## 开发和定制

如需要进行自定义开发，主要修改以下文件：

- `config.py`: 系统配置参数
- `app/models/`: 数据库模型
- `app/routes/`: 业务逻辑和路由
- `app/templates/`: 页面模板

## 许可证

MIT License
