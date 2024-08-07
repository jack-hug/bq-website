from datetime import datetime, timedelta, timezone
import os.path

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, send_from_directory, \
    jsonify, session
from flask_login import current_user, login_user, login_required, logout_user

from bqwebsite.extensions import db
from bqwebsite.models import Admin, Photo, Product, Brand, Category, Subject, News, NewsCategory
from bqwebsite.forms.admin import LoginForm, ProductForm, EditProductForm
from bqwebsite.utils import random_filename, resize_image, redirect_back, save_uploaded_files

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')  # 首页
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    product_length = Product.query.count()
    news_length = News.query.count()
    photo_length = Photo.query.count()
    brand_length = Brand.query.count()
    return render_template('admin/index.html', product_length=product_length, news_length=news_length,
                           photo_length=photo_length, brand_length=brand_length,
                           last_login_time=current_user.last_login_time)


@admin_bp.route('/login', methods=['GET', 'POST'])  # 登录页面
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            admin = Admin.query.filter_by(email=form.email.data.lower()).first()
            if admin is not None and admin.validate_password(form.password.data):
                admin.last_login_time = datetime.now().replace(microsecond=0)
                db.session.commit()
                if login_user(admin, form.remember_me.data):
                    flash('Login success...', 'info')
                    return redirect(url_for('admin.index'))
                else:
                    flash('Invalid email or password.', 'warning')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')  # 退出登录
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('admin.login'))


@admin_bp.route('/forget-password', methods=['GET', 'POST'])  # 忘记密码
def forget_password():
    return render_template('admin/reset_password.html')


@admin_bp.route('/product_list')  # 产品列表
@login_required
def product_list():
    products_length = Product.query.count()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.order_by(Product.timestamp.desc()).paginate(page=page, per_page=per_page)
    products = pagination.items
    return render_template('admin/product_list.html', products=products, pagination=pagination,
                           products_length=products_length)


@admin_bp.route('/product/new', methods=['GET', 'POST'])  # 新建产品
@login_required
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            product_content=form.product_content.data,
            product_indication=form.product_indication.data,
            category_id=form.category.data,
            brand_id=form.brand.data,
            subject_id=form.subject.data
        )
        db.session.add(product)
        db.session.commit()

        if 'photos' in request.files and request.files['photos'].filename != '':
            photos = save_uploaded_files(request.files, product)
            db.session.add_all(photos)
            db.session.commit()
        flash('添加成功.', 'success')
        return redirect(url_for('admin.product_list'))
    return render_template('admin/product_add.html', form=form)


@admin_bp.route('/product_edit/<int:product_id>', methods=['GET', 'POST'])  # 编辑产品
@login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = EditProductForm(product=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.product_content = form.product_content.data
        product.product_indication = form.product_indication.data
        product.category_id = form.category.data
        product.brand_id = form.brand.data
        product.subject_id = form.subject.data
        utc_now = datetime.utcnow()
        local_tz = timezone(timedelta(hours=8))  # 设置本地时区为 UTC+8
        local_now = utc_now.replace(tzinfo=timezone.utc).astimezone(local_tz)
        product.timestamp = local_now
        if 'photos' in request.files and request.files['photos'].filename != '':
            photos = save_uploaded_files(request.files, product)
            db.session.add_all(photos)
            db.session.commit()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.product_list'))
    elif form.cancel.data:
        return redirect(url_for('admin.product_list'))
    form.name.data = product.name
    form.product_content.data = product.product_content
    form.product_indication.data = product.product_indication
    form.category.data = product.category_id
    form.brand.data = product.brand_id
    form.subject.data = product.subject_id
    return render_template('admin/product_edit.html', product=product, form=form)


@admin_bp.route('/uploads/<path:filename>')  # 获得上传图片
@login_required
def get_image(filename):
    return send_from_directory(current_app.config['BQ_UPLOAD_PATH'], filename)


@admin_bp.route('/check_product_name', methods=['GET'])  # 检查产品名称
def check_product_name():
    name = request.args.get('name')
    exists = Product.query.filter_by(name=name).first() is not None
    return jsonify(exists=exists)


@admin_bp.route('/product_delete/<int:product_id>', methods=['POST'])  # 删除产品
@login_required
def product_delete(product_id):
    product_id = Product.query.get_or_404(product_id)
    db.session.delete(product_id)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect_back()


@admin_bp.route('/product_status/<int:product_id>')  # 发布与撤销
@login_required
def product_status(product_id):
    product = Product.query.get_or_404(product_id)
    product.status = not product.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/category_list', methods=['GET', 'POST'])  # 分类列表
@login_required
def category_list():
    return render_template('admin/category_list.html')


@admin_bp.route('/brand_edit/<int:brand_id>', methods=['GET', 'POST'])  # 编辑商标
@login_required
def brand_edit(brand_id):
    brand_id = Brand.query.get_or_404(brand_id)
    return render_template('admin/category_edit.html', brand_id=brand_id)


@admin_bp.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])  # 编辑分类
@login_required
def category_edit(category_id):
    category_id = Category.query.get_or_404(category_id)
    return render_template('admin/category_edit.html', category_id=category_id)


@admin_bp.route('/subject_edit/<int:subject_id>', methods=['GET', 'POST'])  # 编辑功能主治
@login_required
def subject_edit(subject_id):
    subject_id = Subject.query.get_or_404(subject_id)
    return render_template('admin/category_edit.html', subject_id=subject_id)


@admin_bp.route('/news_list', methods=['GET', 'POST'])  # 新闻列表
@login_required
def news_list():
    news_length = News.query.count()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = News.query.order_by(News.timestamp.desc()).paginate(page=page, per_page=per_page)
    news = pagination.items
    return render_template('admin/news_list.html', news=news, pagination=pagination, news_length=news_length)


@admin_bp.route('/news_category_list', methods=['GET', 'POST'])  # 新闻分类列表
@login_required
def news_category_list():
    return render_template('admin/news_category_list.html')


@admin_bp.route('/news_edit/<int:news_id>', methods=['GET', 'POST'])  # 编辑新闻
@login_required
def news_edit(news_id):
    news_id = News.query.get_or_404(news_id)
    return render_template('admin/category_edit.html', news_id=news_id)


@admin_bp.route('/news_category_edit/<int:news_category_id>', methods=['GET', 'POST'])  # 编辑新闻分类
@login_required
def news_category_edit(news_category_id):
    news_category_id = NewsCategory.query.get_or_404(news_category_id)
    return render_template('admin/category_edit.html', news_category_id=news_category_id)


@admin_bp.route('/banner_photo_list', methods=['GET', 'POST'])  # 轮播图列表
@login_required
def banner_photo_list():
    return render_template('admin/banner_photo_list.html')


@admin_bp.route('/scroll_photo_list', methods=['GET', 'POST'])  # 滚动图片列表
@login_required
def scroll_photo_list():
    return render_template('admin/scroll_photo_list.html')


@admin_bp.route('/category_photo_list', methods=['GET', 'POST'])  # 分类图片列表
@login_required
def category_photo_list():
    return render_template('admin/category_photo_list.html')


@admin_bp.route('/index_photo_list', methods=['GET', 'POST'])  # 首页其他图片
@login_required
def index_photo_list():
    return render_template('admin/index_photo_list.html')


@admin_bp.route('/introduce_list', methods=['GET', 'POST'])  # 公司介绍列表
@login_required
def introduce_list():
    return render_template('admin/introduce_list.html')

# @admin_bp.route('/banner_photo_list/<int:photo_id>', methods=['GET', 'POST'])
# @login_required
# def banner_photo_list(photo_id):
#     photo_id = Photo.query.get_or_404(photo_id)
#     return render_template('admin/banner_photo_edit.html', photo_id=photo_id)
#
# @admin_bp.route('/scroll_photo_list/<int:photo_id>', methods=['GET', 'POST'])
# @login_required
# def scroll_photo_list(photo_id):
#     photo_id = Photo.query.get_or_404(photo_id)
#     return render_template('admin/scroll_photo_edit.html', photo_id=photo_id)
#
# @admin_bp.route('/category_photo_list/<int:photo_id>', methods=['GET', 'POST'])
# @login_required
# def category_photo_list(photo_id):
#     photo_id = Photo.query.get_or_404(photo_id)
#     return render_template('admin/category_photo_edit.html', photo_id=photo_id)
#
# @admin_bp.route('/index_photo_list/<int:photo_id>', methods=['GET', 'POST'])
# @login_required
# def index_photo_list(photo_id):
#     photo_id = Photo.query.get_or_404(photo_id)
#     return render_template('admin/index_photo_edit.html', photo_id=photo_id)
