import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig:
    BQ_ADMIN_EMAIL = os.getenv('BQ_ADMIN')
    BQ_PRODUCT_PER_PAGE = 12
    BQ_NEWS_PER_PAGE = 12
    BQ_PHOTO_PER_PAGE = 12
    BQ_NOTIFICATION_PER_PAGE = 20
    BQ_MANAGE_PHOTO_PER_PAGE = 20
    BQ_MANAGE_CATEGORY_PER_PAGE = 20
    BQ_SEARCH_RESULT_PER_PAGE = 30
    BQ_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    BQ_TEMP_FOLDER = os.path.join(basedir, 'temp')
    if not os.path.exists(BQ_UPLOAD_PATH):
        os.mkdir(BQ_UPLOAD_PATH)
    BQ_PHOTO_SIZE = {
        'small': 100,
        'medium': 600
    }
    BQ_PHOTO_SUFFIX = {
        BQ_PHOTO_SIZE['small']: '_s',
        BQ_PHOTO_SIZE['medium']: '_m'
    }

    SECRET_KEY = os.getenv('SECRET_KEY')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 限制整个请求体的大小，而不仅仅是单个文件的大小。

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = 'standard'
    CKEDITOR_HEIGHT = 400
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'  # ckeditor上传图片的函数

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    MOMENT_TIMEZONE = 'Asia/Shanghai'  # 配置moment时区


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
