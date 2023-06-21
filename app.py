from flask import Flask, render_template
from models import Categories, Products, News, Brand, Honor, Banner, Introduce, ProductImage, NewsCategory, IntroduceCategory
from exts import db, admin
from flask_migrate import Migrate
import config
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)


class ProductView(ModelView):
    column_list = ('product_name', 'product_indication', 'product_manual', 'timestamp', 'clicks', 'category.product_category')
    # column_choices = {
    #     'category': [
    #         (Categories.id, '膏剂'),
    #     ]
    # }
    column_labels = {
        'category.product_category': '剂型'
    }

    column_formatters = {
        'category.product_category': Categories.product_category
    }


# class EmployeeView(ModelView):
#
#     column_list = ('name', 'department.name')  # 显示部门名称而不是外键 ID
#
#     column_labels = {
#         'department.name': 'Department'
#     }
#
#     def _department_formatter(self, context, model, name):
#         return model.department.name
#
#     column_formatters = {
#         'department.name': _department_formatter
#     }


app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)
admin.init_app(app)
admin.add_view(ModelView(Products, db.session, name='产品'))
admin.add_view(ModelView(Categories, db.session, name='产品分类'))
admin.add_view(ModelView(News, db.session, name='新闻'))
admin.add_view(ModelView(NewsCategory, db.session, name='新闻分类'))
admin.add_view(ModelView(Brand, db.session, name='商标'))
admin.add_view(ModelView(Honor, db.session, name='公司荣誉'))
admin.add_view(ModelView(Banner, db.session, name='banner图片管理'))
admin.add_view(ModelView(Introduce, db.session, name='公司介绍'))
admin.add_view(ModelView(IntroduceCategory, db.session, name='介绍分类'))
admin.add_view(ModelView(ProductImage, db.session, name='产品图片'))


@app.route('/')
def index():
    intro = Introduce.query.first()
    return render_template('index.html', intro=intro)


@app.route('/news')
def news():
    news_category = NewsCategory.query.all()
    return render_template('news.html', news_category=news_category)


@app.route('/news_company')
def news_company():
    return render_template('news_company.html')


@app.route('/news_industry')
def news_industry():
    return render_template('news_industry.html')


@app.route('/news_file')
def news_file():
    return render_template('news_file.html')


@app.route('/news_detail')
def news_detail():
    return render_template('news_detail.html')


@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/product_categories')
def proudct_categories():
    return render_template('product_categories.html')

@app.route('/product_detail')
def product_detail():
    return render_template('product_detail.html')


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/introduce_company')
def introduce_company():
    return render_template('introduce_company.html')


@app.route('/introduce_quality')
def introduce_quality():
    return render_template('introduce_quality.html')


@app.route('/introduce_structure')
def introduce_structure():
    return render_template('introduce_structure.html')


@app.route('/introduce_responsibility')
def introduce_responsibility():
    return render_template('introduce_responsibility.html')


@app.route('/honor')
def honor():
    return render_template('honor.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/contact_cooperate')
def contact_cooperate():
    return render_template('contact_cooperate.html')


@app.route('/contact_recruit')
def contact_recruit():
    return render_template('contact_recruit.html')


if __name__ == '__main__':
    app.run()
