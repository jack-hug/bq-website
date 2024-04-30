import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig:
    BQ_ADMIN_EMAIL = os.getenv('BQ_ADMIN', '46361381@qq.com')
    BQ_NEWS_PER_PAGE = 12
    BQ_PHOTO_PER_PAGE = 12
    BQ_NOTIFICATION_PER_PAGE = 20
    BQ_MANAGE_PHOTO_PER_PAGE = 20
    BQ_MANAGE_CATEGORY_PER_PAGE = 20
    BQ_SEARCH_RESULT_PER_PAGE = 30
    BQ_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BQ_PHOTO_SIZE = {
        'small': 400,
        'medium': 800
    }
    BQ_PHOTO_SUFFIX = {
        BQ_PHOTO_SIZE['small']: '_s',
        BQ_PHOTO_SIZE['medium']: '_m'
    }

    SECRET_KEY = os.getenv('SECRET_KEY')

    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 30
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_ENABLE_CSRF = True

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'bq-data-dev.db')


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'bq-data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

