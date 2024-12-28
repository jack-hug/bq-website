import os
from datetime import datetime

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, send_from_directory, \
    jsonify, session
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_user, login_required, logout_user

from ..extensions import db
from ..models import Admin, Photo, Product, Brand, Category, Subject, News, NewsCategory
from ..forms.admin import LoginForm, ProductForm, EditProductForm, CategoryForm, BrandForm, SubjectForm, \
    EditCategoryForm
from ..utils import random_filename, redirect_back, save_uploaded_files

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
                admin.last_login_time = datetime.utcnow().replace(microsecond=0)
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
                           products_length=products_length, show_collapse=True)


@admin_bp.route('/product/new', methods=['GET', 'POST'])  # 新建产品
@login_required
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            product_content=form.product_content.data,
            product_indication=form.product_indication.data,
            product_format=form.product_format.data,
            category_id=form.category.data,
            brand_id=form.brand.data,
            subject_id=form.subject.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(product)
        db.session.commit()
        flash('添加成功.', 'success')
        return redirect(url_for('admin.product_list'))
    return render_template('admin/product_add.html', form=form, show_collapse=True)


@admin_bp.route('/product_edit/<int:product_id>', methods=['GET', 'POST'])  # 编辑产品
@login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    form = EditProductForm(product=product)
    if form.validate_on_submit():
        product.name = form.name.data
        product.product_content = form.product_content.data
        product.product_indication = form.product_indication.data
        product.product_format = form.product_format.data
        product.category_id = form.category.data
        product.brand_id = form.brand.data
        product.subject_id = form.subject.data
        product.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.product_list'))
    elif form.cancel.data:
        return redirect(url_for('admin.product_list'))
    form.name.data = product.name
    form.product_content.data = product.product_content
    form.product_indication.data = product.product_indication
    form.product_format.data = product.product_format
    form.category.data = product.category_id
    form.brand.data = product.brand_id
    form.subject.data = product.subject_id
    return render_template('admin/product_edit.html', product=product, form=form, show_collapse=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@admin_bp.route('/upload_image', methods=['POST'])  # flask_ckeditor上传图片
@login_required
def upload_image():
    f = request.files.get('upload')
    if not allowed_file(f.filename):
        return upload_fail(message='错误的文件格式！只能上传png, jpg, jpeg, gif格式文件')
    filename = random_filename(f.filename)
    f.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
    url = url_for('admin.get_image', filename=filename)

    return upload_success(url=url)


@admin_bp.route('/product_photo_upload', methods=['POST'])  # dropzone上传图片并绑定product.id
@login_required
def product_photo_upload():
    product_id = request.form.get('product_id')
    if 'file' not in request.files:
        return jsonify(message='没有文件或者文件出错'), 400
    if request.files['file'].filename == '':
        return jsonify(message='没有上传文件'), 400
    if not allowed_file(request.files.get('file')):
        return jsonify(message='错误的文件格式！只能上传png, jpg, jpeg, gif格式文件'), 400
    try:
        photos = save_uploaded_files(request.files, product_id)
        db.session.add_all(photos)
        db.session.commit()
        return jsonify(message='图片上传成功', filenames=[photo.filename for photo in photos])
    except Exception as e:
        db.session.rollback()
        return jsonify(message='上传失败', error=str(e)), 400


# @admin_bp.route('/product_photo_upload', methods=['POST'])  # dropzone上传图片
# @login_required
# def product_photo_upload():
#     f = request.files.get('file')
#     if not allowed_file(f.filename):
#         return jsonify(message='错误的文件格式！只能上传png, jpg, jpeg, gif格式文件'), 400
#     filename = random_filename(f.filename)
#     f.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
#     url = url_for('admin.get_image', filename=filename)
#     return jsonify(filename=filename, uploaded=1, url=url)


@admin_bp.route('/uploads/<path:filename>')  # 获得上传图片
def get_image(filename):
    upload_path = current_app.config['BQ_UPLOAD_PATH']
    file_path = os.path.join(upload_path, filename)
    if not os.path.exists(file_path):
        return 'File not found', 404
    return send_from_directory(current_app.config['BQ_UPLOAD_PATH'], filename)


@admin_bp.route('/check_product_name', methods=['POST'])  # 检查产品名称
def check_product_name():
    name = request.json.get('name')
    exists = Product.query.filter_by(name=name).first() is not None
    return jsonify(exists=exists)


@admin_bp.route('/product_delete/<int:product_id>', methods=['POST'])  # 删除产品
@login_required
def product_delete(product_id):
    product = Product.query.get_or_404(product_id)
    product.delete_product()
    flash('删除成功.', 'success')
    return redirect_back()


@admin_bp.route('/product_multiple_delete', methods=['GET', 'POST'])  # 批量删除
@login_required
def product_multiple_delete():
    if request.method == 'POST':
        selected_ids = request.form.getlist('item_ids')
        for product_id in selected_ids:
            product = Product.query.get(product_id)
            db.session.delete(product)
        db.session.commit()
        flash('批量删除成功.', 'success')
        return redirect(url_for('admin.product_list'))
    return redirect(url_for('admin.product_list'))


@admin_bp.route('/photo_delete/<int:photo_id>', methods=['POST'])  # 删除图片
@login_required
def photo_delete(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    try:
        os.remove(os.path.join(current_app.config['BQ_UPLOAD_PATH'], photo.filename))
    except OSError as e:
        return jsonify(success=False), 500

    db.session.delete(photo)
    db.session.commit()
    print('delete...')
    return jsonify(success=True)


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
    return render_template('admin/category_list.html', show_collapse=True)


@admin_bp.route('/category_add', methods=['GET', 'POST'])  # 新建分类
@login_required
def category_add():
    category_form = CategoryForm()
    brand_form = BrandForm()
    subject_form = SubjectForm()
    if request.method == 'POST':
        if category_form.category_submit.data and category_form.validate():
            category = Category(
                name=category_form.name.data,
                timestamp=datetime.utcnow()
            )
            db.session.add(category)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.category_list'))
        if brand_form.brand_submit.data and brand_form.validate():
            brand = Brand(
                name=brand_form.name.data,
                timestamp=datetime.utcnow()
            )
            db.session.add(brand)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.category_list'))
        if subject_form.subject_submit.data and subject_form.validate():
            subject = Subject(
                name=subject_form.name.data,
                timestamp=datetime.utcnow()
            )
            db.session.add(subject)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.category_list'))
        else:
            flash('添加失败,名称已经存在', 'info')
            return redirect(url_for('admin.category_add'))
    return render_template('admin/category_add.html', category_form=category_form, brand_form=brand_form,
                           subject_form=subject_form, show_collapse=True)


@admin_bp.route('/brand_edit/<int:brand_id>', methods=['GET', 'POST'])  # 编辑商标
@login_required
def brand_edit(brand_id):
    brand_id = Brand.query.get_or_404(brand_id)
    return render_template('admin/brand_edit.html', brand_id=brand_id)


@admin_bp.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])  # 编辑分类
@login_required
def category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    form = EditCategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        category.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.category_list'))
    form.name.data = category.name
    return render_template('admin/category_edit.html', category=category, form=form)


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
