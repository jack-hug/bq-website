from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_moment import Moment


bootstrap = Bootstrap5()
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
ckeditor = CKEditor()
migrate = Migrate()
moment = Moment()


@login_manager.user_loader
def load_user(user_id):
    from .models import Admin
    user = Admin.query.get(int(user_id))
    return user


