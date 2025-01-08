import json
import os
import time
from datetime import datetime

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, send_from_directory, \
    jsonify, session, abort
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_user, login_required, logout_user

from ..extensions import db
from ..models import Admin, Photo, Product, Brand, Category, Subject, News, NewsCategory
from ..forms.admin import LoginForm, ProductForm, EditProductForm, EditCategoryForm, EditBrandForm, CategoryAddForm, \
    BrandAddForm, SubjectAddForm, EditSubjectForm
from ..utils import random_filename, redirect_back, resize_image, save_temp_files

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

        temp_files = request.form.get('temp_files')
        temp_files = json.loads(temp_files)
        if temp_files:
            for temp_file in temp_files:
                temp_path = os.path.join(current_app.config['BQ_TEMP_FOLDER'], temp_file)
                final_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], temp_file)
                os.rename(temp_path, final_path)

                photo = Photo(
                    filename=temp_file,
                    filename_m=resize_image(final_path, temp_file, current_app.config['BQ_PHOTO_SIZE']['medium'],
                                            current_app.config['BQ_PHOTO_SIZE']['medium']),
                    filename_s=resize_image(final_path, temp_file, current_app.config['BQ_PHOTO_SIZE']['small'],
                                            current_app.config['BQ_PHOTO_SIZE']['small']),
                    product_id=product.id
                )
                db.session.add(photo)
            db.session.commit()

        flash('添加成功.', 'success')
        return redirect(url_for('admin.product_list'))
    return render_template('admin/product_add.html', form=form, show_collapse=True)


@admin_bp.route('/product_edit/<int:product_id>', methods=['GET', 'POST'])  # 编辑产品
@login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    photos = Photo.query.filter_by(product_id=product_id).all()
    form = EditProductForm(product=product)

    if form.cancel.data:
        return redirect(url_for('admin.product_list'))
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

        temp_files = request.form.get('temp_files')
        temp_files = json.loads(temp_files)
        if temp_files:
            for temp_file in temp_files:
                temp_path = os.path.join(current_app.config['BQ_TEMP_FOLDER'], temp_file)
                final_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], temp_file)
                os.rename(temp_path, final_path)

                photo = Photo(
                    filename=temp_file,
                    filename_m=resize_image(final_path, temp_file, current_app.config['BQ_PHOTO_SIZE']['medium'],
                                            current_app.config['BQ_PHOTO_SIZE']['medium']),
                    filename_s=resize_image(final_path, temp_file, current_app.config['BQ_PHOTO_SIZE']['small'],
                                            current_app.config['BQ_PHOTO_SIZE']['small']),
                    product_id=product.id
                )
                db.session.add(photo)
            db.session.commit()

        flash('修改成功.', 'success')
        return redirect(url_for('admin.product_list'))
    form.name.data = product.name
    form.product_content.data = product.product_content
    form.product_indication.data = product.product_indication
    form.product_format.data = product.product_format
    form.category.data = product.category_id
    form.brand.data = product.brand_id
    form.subject.data = product.subject_id
    return render_template('admin/product_edit.html', product=product, photos=photos, form=form, show_collapse=True)


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
    if 'file' not in request.files:
        return jsonify(message='没有文件或者文件出错'), 400
    if request.files['file'].filename == '':
        return jsonify(message='没有上传文件'), 400
    if not allowed_file(request.files['file'].filename):
        return jsonify(message='错误的文件格式！只能上传png, jpg, jpeg, gif格式文件'), 400
    filename = save_temp_files(request.files['file'])
    return jsonify(message='上传成功', filename=filename)


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
    category_add_form = CategoryAddForm()
    brand_add_form = BrandAddForm()
    subject_add_form = SubjectAddForm()
    if request.method == 'POST':
        if category_add_form.category_submit.data and category_add_form.validate():
            category = Category(
                name=category_add_form.name.data,
                status=True,
                timestamp=datetime.utcnow()
            )
            db.session.add(category)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.category_list'))
        if brand_add_form.brand_submit.data and brand_add_form.validate():
            brand = Brand(
                name=brand_add_form.name.data,
                status=True,
                timestamp=datetime.utcnow()
            )
            db.session.add(brand)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.category_list'))
        if subject_add_form.subject_submit.data and subject_add_form.validate():
            subject = Subject(
                name=subject_add_form.name.data,
                status=True,
                timestamp=datetime.utcnow()
            )
            db.session.add(subject)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.category_list'))
    return render_template('admin/category_list.html', category_add_form=category_add_form,
                           brand_add_form=brand_add_form, subject_add_form=subject_add_form, show_collapse=True)

@admin_bp.route('/category_status/<int:category_id>')  # 分类发布与撤销
@login_required
def category_status(category_id):
    category = Category.query.get_or_404(category_id)
    category.status = not category.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/brand_status/<int:brand_id>')  # 商标发布与撤销
@login_required
def brand_status(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    brand.status = not brand.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/subject_status/<int:subject_id>')  # 功能主治发布与撤销
@login_required
def subject_status(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    subject.status = not subject.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/brand_edit/<int:brand_id>', methods=['GET', 'POST'])  # 编辑商标
@login_required
def brand_edit(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    form = EditBrandForm()
    if form.validate_on_submit():
        brand.name = form.name.data
        brand.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.category_list'))
    form.name.data = brand.name
    return render_template('admin/brand_edit.html', brand=brand, form=form)


@admin_bp.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])  # 编辑分类
@login_required
def category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    form = EditCategoryForm(category_id=category.id)
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
    subject = Subject.query.get_or_404(subject_id)
    form = EditSubjectForm(subject_id=subject.id)
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.category_list'))
    form.name.data = subject.name
    return render_template('admin/subject_edit.html', subject=subject, form=form)


@admin_bp.route('/category_delete/<int:category_id>', methods=['GET', 'POST'])  # 删除分类
@login_required
def category_delete(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.category_list'))

@admin_bp.route('/brand_delete/<int:brand_id>', methods=['GET', 'POST'])  # 删除商标
@login_required
def brand_delete(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    db.session.delete(brand)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.category_list'))

@admin_bp.route('/subject_delete/<int:subject_id>', methods=['GET', 'POST'])  # 删除功能
@login_required
def subject_delete(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.category_list'))


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


# 类型与数据表的映射
MODEL_MAP = {
    'category-input': Category,
    'brand-input': Brand,
    'subject-input': Subject,
}
@admin_bp.route('/check_category_name', methods=['POST'])  # 检查分类名称是否已经存在
def check_category_name():
    data = request.get_json()
    name = data.get('name')
    check_type = data.get('type')
    model = MODEL_MAP.get(check_type)
    if not model:
        return jsonify({'exists': False}), 400

    exists = model.query.filter_by(name=name).first() is not None
    return jsonify({'exists': exists})
