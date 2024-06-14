from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
from flask_dropzone import Dropzone


bootstrap = Bootstrap5()
db = SQLAlchemy()
csrf = CSRFProtect()
dropzone = Dropzone()
