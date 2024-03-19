from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect


bootstrap = Bootstrap5()
db = SQLAlchemy()
csrf = CSRFProtect()
