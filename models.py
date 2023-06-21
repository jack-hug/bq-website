from exts import db
from datetime import datetime


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_category = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    products = db.relationship('Products', back_populates='category')


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100))
    product_indication = db.Column(db.String(200))
    product_manual = db.Column(db.Text)
    product_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    clicks = db.Column(db.Integer, default=0)

    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Categories', back_populates='products')

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', back_populates='products')

    productimage = db.relationship('ProductImage', back_populates='products')


class ProductImage(db.Model):
    __tablename__ = 'productimage'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)

    products_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    products = db.relationship('Products', back_populates='productimage')


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_title = db.Column(db.String(100))
    news_content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    newscategory_id = db.Column(db.Integer, db.ForeignKey('newscategory.id'))
    newscategory = db.relationship('NewsCategory', back_populates='news')


class NewsCategory(db.Model):
    __tablename__ = 'newscategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_categories = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)
    news = db.relationship('News', back_populates='newscategory')


class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now, index=True)


class Honor(db.Model):
    __tablename__ = 'honor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    honor_title = db.Column(db.String(100))
    honor_img = db.Column(db.String(200))


class Brand(db.Model):
    __tablename__ = 'brand'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    brand_name = db.Column(db.String(100))
    brand_category = db.Column(db.String(100))

    products = db.relationship('Products', back_populates='brand')


class Introduce(db.Model):
    __tablename__ = 'introduce'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list = db.Column(db.String(100))
    introduce_content = db.Column(db.Text)
    introduce_category_id = db.Column(db.Integer, db.ForeignKey('introducecategory.id'))
    introduce_category = db.relationship('IntroduceCategory', back_populates='introduce')


class IntroduceCategory(db.Model):
    __tablename__ = 'introducecategory'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    introduce_category = db.Column(db.String(100))
    introduce = db.relationship('Introduce', back_populates='introduce_category')

