from bqwebsite.extensions import db
from datetime import datetime


class Category(db.Model):
    # 产品剂型分类
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_category = db.Column(db.String(100), nullable=False)  # 产品分类名称
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    products = db.relationship('Products', back_populates='category')


class Product(db.Model):
    # 产品
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100))  # 品名
    product_indication = db.Column(db.String(200))  # 功能主治
    product_manual = db.Column(db.Text)  # 说明书
    product_content = db.Column(db.Text)  # 产品页内容
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    clicks = db.Column(db.Integer, default=0)  # 点击数

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='products')

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', back_populates='products')

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', back_populates='products')

    photos = db.relationship('Photo', back_populates='product')


class Photo(db.Model):
    # 图片
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(128))
    filename_s = db.Column(db.String(128))
    filename_m = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='photos')


class New(db.Model):
    # 新闻
    __tablename__ = 'new'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    newcategory_id = db.Column(db.Integer, db.ForeignKey('newcategory.id'))
    newcategory = db.relationship('NewsCategory', back_populates='news')


class NewCategory(db.Model):
    # 新闻分类
    __tablename__ = 'newcategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_categories = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    news = db.relationship('News', back_populates='newcategory')


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
    brand_name = db.Column(db.String(100))
    brand_category = db.Column(db.String(100))

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
    introduce_category = db.Column(db.String(100))

    introduces = db.relationship('Introduce', back_populates='introduce_category')

class Subject(db.Model):
    # 门科分类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    products = db.relationship('Product', back_populates='subject')
