from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_dropzone import Dropzone
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


bootstrap = Bootstrap5()
db = SQLAlchemy()
csrf = CSRFProtect()
dropzone = Dropzone()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from bqwebsite.models import Admin
    user = Admin.query.get(int(user_id))
    return user


