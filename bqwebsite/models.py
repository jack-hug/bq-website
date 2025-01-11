import os
import re

from flask import current_app
from sqlalchemy import event
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .extensions import db
from datetime import datetime


class Category(db.Model):
    # 产品剂型分类
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # 产品分类名称
    status = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    @staticmethod
    def get_default_category():  # 添加默认分类
        default_category = Category.query.filter_by(name='未分类').first()
        if not default_category:
            default_category = Category(name='未分类')
            db.session.add(default_category)
            db.session.commit()
        return default_category

    products = db.relationship('Product', back_populates='category')


class Product(db.Model):
    # 产品
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)  # 品名
    product_indication = db.Column(db.String(200))  # 功能主治
    product_content = db.Column(db.Text)  # 产品页内容
    product_format = db.Column(db.String(100))  # 产品规格
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    clicks = db.Column(db.Integer, default=0)  # 点击数
    status = db.Column(db.Boolean, default=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))  # 按剂型分类
    category = db.relationship('Category', back_populates='products')

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))  # 按商标分类
    brand = db.relationship('Brand', back_populates='products')

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))  # 按功能分类
    subject = db.relationship('Subject', back_populates='products')

    photos = db.relationship('Photo', back_populates='product', lazy='dynamic', cascade='all, delete-orphan')

    def delete_product(self):  # 删除产品时删除图片
        self.delete_ckeditor_images()

        for photo in self.photos:
            photo.photos_delete()

        db.session.delete(self)
        db.session.commit()

    def delete_ckeditor_images(self):
        image_paths = self.extract_image_paths(self.product_content)
        for path in image_paths:
            self.delete_image_file(path)

    @staticmethod
    def extract_image_paths(html):
        img_pattern = re.compile(r'<img[^>]+src="([^">]+)"')
        image_paths = img_pattern.findall(html)
        image_paths = [path.lstrip('/admin') for path in image_paths]
        print('image_paths:', image_paths)
        return image_paths

    @staticmethod
    def delete_image_file(relative_path):
        # 去掉 relative_path 中的 'uploads' 部分
        if relative_path.startswith('uploads/'):
            relative_path = relative_path[len('uploads/'):]
        file_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], relative_path)
        file_path = os.path.normpath(file_path)
        print('file_path:', file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print('文件不存在')


class Photo(db.Model):
    # 图片
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(256), unique=True)   # 600*800 上传图片裁剪后尺寸
    filename_s = db.Column(db.String(256), unique=True)  # 300*400 产品中心缩略图
    filename_m = db.Column(db.String(256), unique=True)  # 450*600 首页分类及缩略图
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='photos')

    def photos_delete(self):  #
        upload_path = current_app.config['BQ_UPLOAD_PATH']
        for filename in [self.filename, self.filename_s, self.filename_m]:
            if filename:
                file_path = os.path.join(upload_path, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)


class News(db.Model):
    # 新闻
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    status = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    clicks = db.Column(db.Integer, default=0)  # 点击数

    newscategory_id = db.Column(db.Integer, db.ForeignKey('newscategory.id'))
    newscategory = db.relationship('NewsCategory', back_populates='news')


class NewsCategory(db.Model):
    # 新闻分类
    __tablename__ = 'newscategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    status = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    news = db.relationship('News', back_populates='newscategory', cascade='all, delete-orphan')


class Banner(db.Model):
    # 轮播图片
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)


class Honor(db.Model):
    # 企业荣誉
    __tablename__ = 'honor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    honor_title = db.Column(db.String(100))
    honor_img = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)


class Brand(db.Model):
    # 商标，与产品多对多
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    @staticmethod
    def get_default_brand():  # 添加默认商标分类
        default_brand = Brand.query.filter_by(name='未分类').first()
        if not default_brand:
            default_brand = Brand(name='未分类')
            db.session.add(default_brand)
            db.session.commit()
        return default_brand

    products = db.relationship('Product', back_populates='brand')


class Introduce(db.Model):
    # 公司简介
    __tablename__ = 'introduce'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    introduce_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    introduce_category_id = db.Column(db.Integer, db.ForeignKey('introducecategory.id'))
    introduce_category = db.relationship('IntroduceCategory', back_populates='introduces')


class IntroduceCategory(db.Model):
    # 公司介绍分类
    __tablename__ = 'introducecategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    introduces = db.relationship('Introduce', back_populates='introduce_category')

class ResearchCategory(db.Model):
    # 研发生产分类
    __tablename__ = 'researchcategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    researchs = db.relationship('Research', back_populates='research_category')


class Research(db.Model):
    # 研发生产
    __tablename__ = 'research'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    research_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    research_category_id = db.Column(db.Integer, db.ForeignKey('researchcategory.id'))
    research_category = db.relationship('ResearchCategory', back_populates='researchs')

class Subject(db.Model):
    # 功能分类
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    status = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    @staticmethod
    def get_default_subject():  # 添加默认功能分类
        default_subject = Subject.query.filter_by(name='未分类').first()
        if not default_subject:
            default_subject = Subject(name='未分类')
            db.session.add(default_subject)
            db.session.commit()
        return default_subject

    products = db.relationship('Product', back_populates='subject')

class Admin(db.Model, UserMixin):
    # 管理员
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(50))
    last_login_time = db.Column(db.DateTime)  # 最后一次登录时间
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
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    contact_category_id = db.Column(db.Integer, db.ForeignKey('contactcategory.id'))
    contact_category = db.relationship('ContactCategory', back_populates='contacts')

class ContactCategory(db.Model):
    # 联系我们分类
    __tablename__ = 'contactcategory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    contacts = db.relationship('Contact', back_populates='contact_category')


@event.listens_for(Photo, 'after_delete')
def photo_delete_files(mapper, connection, target):
    target.photos_delete()


