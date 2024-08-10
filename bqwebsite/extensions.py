from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_dropzone import Dropzone
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_ckeditor import CKEditor


bootstrap = Bootstrap5()
db = SQLAlchemy()
csrf = CSRFProtect()
dropzone = Dropzone()
login_manager = LoginManager()
ckeditor = CKEditor()


@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    user = Admin.query.get(int(user_id))
    return user


