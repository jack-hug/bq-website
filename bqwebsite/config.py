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
    BQ_PRODUCT_PER_PAGE = 12
    BQ_NEWS_PER_PAGE = 12
    BQ_PHOTO_PER_PAGE = 12
    BQ_NOTIFICATION_PER_PAGE = 20
    BQ_MANAGE_PHOTO_PER_PAGE = 20
    BQ_MANAGE_CATEGORY_PER_PAGE = 20
    BQ_SEARCH_RESULT_PER_PAGE = 30
    BQ_UPLOAD_PATH = os.path.join(basedir, 'uploads')
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

    SECRET_KEY = os.getenv('SECRET_KEY', 'jackhunghuangbqwebguangwang')
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = 'standard'
    CKEDITOR_HEIGHT = 400
    # CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    # DROPZONE_MAX_FILE_SIZE = 3
    # DROPZONE_MAX_FILES = 30
    # DROPZONE_ALLOWED_FILE_TYPE = 'image'
    # DROPZONE_ENABLE_CSRF = True
    # DROPZONE_INVALID_FILE_TYPE = '文件类型错误，请使用.jpg或者.png格式'
    # DROPZONE_FILE_TOO_BIG = '文件过大 {{ filesize }}，文件最大尺寸不得超过{{ maxFilesize }}M'
    # DROPZONE_DEFAULT_MESSAGE = '将文件拖动到这里或者点击上传，文件大小不得超过3M，文件数量不得超过30个'


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
