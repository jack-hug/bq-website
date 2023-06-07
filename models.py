from exts import db
from datetime import datetime


class Categories(db.Model):
    __tablename__ = 'product_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_categories = db.Column(db.String(100), nullable=True)
    products = db.relationship('Products', back_populates='category')


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100))
    product_manual = db.Column(db.Text)
    product_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.now, index=True)
    categories_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    category = db.relationship('Categories', back_populates='products')
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', back_populates='products')


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_title = db.Column(db.String(100))
    news_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.now, index=True)


class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    banner_img = db.Column(db.String(200))

class Honor(db.Model):
    __tablename__ = 'honor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    honor_img = db.Column(db.String(200))


class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.String(100))
    products = db.relationship('Products', back_populates='brand')


class Introduce(db.Model):
    __tablename__ = 'introduce'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list = db.Column(db.String(100))
    introduce_content = db.Column(db.Text)
