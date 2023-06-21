from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()
admin = Admin(name='邦琪官网后台管理', template_mode='bootstrap3')
