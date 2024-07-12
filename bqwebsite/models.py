from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from bqwebsite.extensions import db
from datetime import datetime


class Category(db.Model):
    # 产品剂型分类
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # 产品分类名称
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    products = db.relationship('Product', back_populates='category')


class Product(db.Model):
    # 产品
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))  # 品名
    product_indication = db.Column(db.String(200))  # 功能主治
    product_manual = db.Column(db.Text)  # 说明书
    product_content = db.Column(db.Text)  # 产品页内容
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    clicks = db.Column(db.Integer, default=0)  # 点击数

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 按剂型分类
    category = db.relationship('Category', back_populates='products')

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))  # 按商标分类
    brand = db.relationship('Brand', back_populates='products')

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))  # 按功能分类
    subject = db.relationship('Subject', back_populates='products')

    photos = db.relationship('Photo', back_populates='product', cascade='all')


class Photo(db.Model):
    # 图片
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(128))   # 600*800 上传图片裁剪后尺寸
    filename_s = db.Column(db.String(128))  # 300*400 产品中心缩略图
    filename_m = db.Column(db.String(128))  # 450*600 首页分类及缩略图
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='photos')


class News(db.Model):
    # 新闻
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    clicks = db.Column(db.Integer, default=0)  # 点击数

    newscategory_id = db.Column(db.Integer, db.ForeignKey('newscategory.id'))
    newscategory = db.relationship('NewsCategory', back_populates='news')


class NewsCategory(db.Model):
    # 新闻分类
    __tablename__ = 'newscategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    news = db.relationship('News', back_populates='newscategory')


class Banner(db.Model):
    # 轮播图片
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)


class Honor(db.Model):
    # 企业荣誉
    __tablename__ = 'honor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    honor_title = db.Column(db.String(100))
    honor_img = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)


class Brand(db.Model):
    # 商标，与产品多对多
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    products = db.relationship('Product', back_populates='brand')


class Introduce(db.Model):
    # 公司简介
    __tablename__ = 'introduce'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    introduce_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    introduce_category_id = db.Column(db.Integer, db.ForeignKey('introducecategory.id'))
    introduce_category = db.relationship('IntroduceCategory', back_populates='introduces')


class IntroduceCategory(db.Model):
    # 公司介绍分类
    __tablename__ = 'introducecategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    introduces = db.relationship('Introduce', back_populates='introduce_category')

class Subject(db.Model):
    # 功能分类
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    products = db.relationship('Product', back_populates='subject')

class Admin(db.Model, UserMixin):
    # 管理员
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

class Contact(db.Model):
    # 联系我们
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)

    contact_category_id = db.Column(db.Integer, db.ForeignKey('contactcategory.id'))
    contact_category = db.relationship('ContactCategory', back_populates='contacts')

class ContactCategory(db.Model):
    # 联系我们分类
    __tablename__ = 'contactcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    contacts = db.relationship('Contact', back_populates='contact_category')


