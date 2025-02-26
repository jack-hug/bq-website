import json
import os
import time
from datetime import datetime

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, send_from_directory, \
    jsonify, session, abort
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.exceptions import BadRequest

from .. import models
from ..extensions import db
from ..models import Admin, Photo, Product, Brand, Category, Subject, News, NewsCategory, Introduce, IntroduceCategory, \
    ResearchCategory, Research, ContactCategory, Contact, Banner, IndexAbout
from ..forms.admin import LoginForm, ProductForm, EditProductForm, EditCategoryForm, EditBrandForm, CategoryAddForm, \
    BrandAddForm, SubjectAddForm, EditSubjectForm, NewsForm, EditNewsForm, EditNewsCategoryForm, AddNewsCategoryForm, \
    EditIntroduceForm, IntroduceAddForm, AddIntroCategoryForm, EditIntroCategoryForm, EditResearchForm, ResearchAddForm, \
    EditContactForm, ContactAddForm, AddContactCategoryForm, EditContactCategoryForm, BannerAddForm, IndexAboutForm
from ..utils import random_filename, redirect_back, resize_image, save_temp_files, save_upload_files

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
                           products_length=products_length, show_product_collapse=True)


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
    return render_template('admin/product_add.html', form=form, show_product_collapse=True)


@admin_bp.route('/product_edit/<int:product_id>', methods=['GET', 'POST'])  # 编辑产品
@login_required
def product_edit(product_id):
    product = Product.query.get_or_404(product_id)
    photos = Photo.query.filter_by(product_id=product_id).all()
    print(photos)
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
    return render_template('admin/product_edit.html', product=product, photos=photos, form=form,
                           show_product_collapse=True)


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


@admin_bp.route('/dropzone_photo_temp_upload', methods=['POST'])  # dropzone上传图片到临时文件夹
@login_required
def dropzone_photo_temp_upload():
    if 'file' not in request.files:
        return jsonify(message='没有文件或者文件出错'), 400
    if request.files['file'].filename == '':
        return jsonify(message='没有上传文件'), 400
    if not allowed_file(request.files['file'].filename):
        return jsonify(message='错误的文件格式！只能上传png, jpg, jpeg, gif格式文件'), 400
    filename = save_temp_files(request.files['file'])
    return jsonify(message='上传成功', filename=filename)


@admin_bp.route('/dropzone_photo_upload', methods=['POST'])  # dropzone上传图片到uploads文件夹
@login_required
def dropzone_photo_upload():
    if 'file' not in request.files:
        return jsonify(message='没有文件或者文件出错'), 400
    if request.files['file'].filename == '':
        return jsonify(message='没有上传文件'), 400
    if not allowed_file(request.files['file'].filename):
        return jsonify(message='错误的文件格式！只能上传png, jpg, jpeg, gif格式文件'), 400
    filename = save_upload_files(request.files['file'])
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


@admin_bp.route('/photo_delete/<int:photo_id>', methods=['POST'])  # 删除产品图片
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
                           brand_add_form=brand_add_form, subject_add_form=subject_add_form, show_product_collapse=True)


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
    return render_template('admin/brand_edit.html', brand=brand, form=form, show_product_collapse=True)


@admin_bp.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])  # 编辑分类
@login_required
def category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    form = EditCategoryForm(category_id=category.id)
    if form.validate_on_submit():
        category.name = form.name.data
        temp_files = json.loads(request.form.get('temp_files'))
        print(temp_files)
        category.filename = temp_files[0] if temp_files else None
        print(category.filename)
        category.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.category_list'))
    form.name.data = category.name
    return render_template('admin/category_edit.html', category=category, form=form, show_product_collapse=True)


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
    return render_template('admin/subject_edit.html', subject=subject, form=form, show_product_collapse=True)


@admin_bp.route('/category_delete/<int:category_id>', methods=['GET', 'POST'])  # 删除分类
@login_required
def category_delete(category_id):
    category = Category.query.get_or_404(category_id)
    default_category = Category.get_default_category()
    Product.query.filter_by(category_id=category.id).update({'category_id': default_category.id})
    db.session.delete(category)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.category_list'))


@admin_bp.route('/brand_delete/<int:brand_id>', methods=['GET', 'POST'])  # 删除商标
@login_required
def brand_delete(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    default_brand = Brand.get_default_brand()
    Product.query.filter_by(brand_id=brand.id).update({'brand_id': default_brand.id})
    db.session.delete(brand)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.category_list'))


@admin_bp.route('/subject_delete/<int:subject_id>', methods=['GET', 'POST'])  # 删除功能
@login_required
def subject_delete(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    default_subject = Subject.get_default_subject()
    Product.query.filter_by(subject_id=subject.id).update({'subject_id': default_subject.id})
    db.session.delete(subject)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.category_list'))


@admin_bp.route('/news_category_delete/<int:news_category_id>', methods=['GET', 'POST'])  # 删除文章分类功能
@login_required
def news_category_delete(news_category_id):
    news_category = NewsCategory.query.get_or_404(news_category_id)
    db.session.delete(news_category)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.news_category_list'))


@admin_bp.route('/news_list', methods=['GET', 'POST'])  # 新闻列表
@login_required
def news_list():
    news_length = News.query.count()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = News.query.order_by(News.timestamp.desc()).paginate(page=page, per_page=per_page)
    news = pagination.items
    return render_template('admin/news_list.html', news=news, pagination=pagination, news_length=news_length,
                           show_news_collapse=True)


@admin_bp.route('/news_category_list', methods=['GET', 'POST'])  # 新闻分类列表
@login_required
def news_category_list():
    form = AddNewsCategoryForm()

    if form.validate_on_submit():
        news_category = NewsCategory.query.filter_by(name=form.name.data.replace(' ', '')).first()
        if news_category:
            flash('该新闻分类已存在.', 'warning')
            return redirect(url_for('admin.news_category_list'))
        else:
            news_category = NewsCategory(
                name=form.name.data,
                timestamp=datetime.utcnow()
            )
            db.session.add(news_category)
            db.session.commit()
            flash('添加成功.', 'success')
            return redirect(url_for('admin.news_category_list'))
    return render_template('admin/news_category_list.html', form=form, show_news_collapse=True)


@admin_bp.route('/news_category_edit/<int:news_category_id>', methods=['GET', 'POST'])  # 编辑新闻分类
@login_required
def news_category_edit(news_category_id):
    news_category = NewsCategory.query.get_or_404(news_category_id)
    form = EditNewsCategoryForm()
    if form.validate_on_submit():
        news_category.name = form.name.data.replace(' ', '')
        news_category.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.news_category_list'))
    form.name.data = news_category.name
    return render_template('admin/news_category_edit.html', news_category_id=news_category_id, form=form,
                           show_news_collapse=True)


@admin_bp.route('/news_category_status/<int:news_category_id>')  # 新闻分类发布与撤销
@login_required
def news_category_status(news_category_id):
    news_category = NewsCategory.query.get_or_404(news_category_id)
    news_category.status = not news_category.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/news_edit/<int:news_id>', methods=['GET', 'POST'])  # 编辑新闻
@login_required
def news_edit(news_id):
    news = News.query.get_or_404(news_id)
    form = EditNewsForm()
    if form.cancel.data:
        return redirect(url_for('admin.news_list'))
    if form.validate_on_submit():
        news.title = form.title.data
        news.newscategory_id = form.newscategory.data
        news.content = form.content.data
        news.timestamp = datetime.utcnow()

        temp_files = request.form.get('temp_files')
        try:
            new_image = json.loads(temp_files) if temp_files else []
        except json.JSONDecodeError:
            new_image = []
        news.filename = new_image

        db.session.add(news)
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.news_list'))
    form.title.data = news.title
    form.newscategory.data = news.newscategory_id
    form.content.data = news.content
    return render_template('admin/news_edit.html', news=news, form=form, show_news_collapse=True)


@admin_bp.route('/news_delete/<int:news_id>', methods=['POST'])  # 删除新闻
@login_required
def news_delete(news_id):
    news = News.query.get_or_404(news_id)
    db.session.delete(news)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.news_list'))


@admin_bp.route('/news/new', methods=['GET', 'POST'])  # 新建文章
@login_required
def news_add():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(
            title=form.title.data,
            newscategory_id=form.newscategory.data,
            content=form.content.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(news)
        db.session.commit()
        flash('添加成功.', 'success')
        return redirect(url_for('admin.news_list'))
    return render_template('admin/news_add.html', form=form, show_collapse=True, show_news_collapse=True)


@admin_bp.route('/news_multiple_delete', methods=['GET', 'POST'])  # 批量删除文章
@login_required
def news_multiple_delete():
    if request.method == 'POST':
        selected_ids = request.form.getlist('item_ids')
        for news_id in selected_ids:
            news = News.query.get(news_id)
            db.session.delete(news)
        db.session.commit()
        flash('批量删除成功.', 'success')
        return redirect(url_for('admin.news_list'))
    return redirect(url_for('admin.news_list'))


@admin_bp.route('/news_status/<int:news_id>')  # 新闻发布与撤销
@login_required
def news_status(news_id):
    news = News.query.get_or_404(news_id)
    news.status = not news.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/banner_photo_list', methods=['GET', 'POST'])  # 轮播图列表
@login_required
def banner_photo_list():
    banner = Banner.query.all()
    return render_template('admin/banner_photo_list.html', banner=banner)


@admin_bp.route('/banner_photo_add', methods=['GET', 'POST'])  # 添加轮播图
@login_required
def banner_photo_add():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "没有文件上传"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400

        # 保存文件到服务器
        filename = random_filename(file.filename)
        file_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename)
        file.save(file_path)

        # 将文件信息保存到数据库
        banner = Banner(
            filename=filename,
            timestamp=datetime.utcnow()
        )
        db.session.add(banner)
        db.session.commit()

        # 返回文件 ID
        return jsonify({"file_id": banner.id}), 200

    return render_template('admin/banner_photo_add.html', show_banner_collapse=True)


@admin_bp.route('/banner_photo_delete/<int:banner_id>', methods=['POST'])  # 删除banner
@login_required
def banner_photo_delete(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    db.session.delete(banner)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.banner_photo_list'))


@admin_bp.route('/banner_multiple_delete', methods=['GET', 'POST'])
@login_required
def banner_multiple_delete():
    if request.method == 'POST':
        selected_ids = request.form.getlist('item_ids')
        for banner_id in selected_ids:
            banner = Banner.query.get(banner_id)
            db.session.delete(banner)
        db.session.commit()
        flash('批量删除成功.', 'success')
        return redirect(url_for('admin.banner_photo_list'))
    return redirect(url_for('admin.banner_photo_list'))


@admin_bp.route('/banner_status/<int:banner_id>', methods=['GET', 'POST'])
@login_required
def banner_photo_status(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    banner.status = not banner.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/dropzone_photo_delete/<int:banner_id>', methods=['DELETE'])  # 在dropzone中删除banner图片
def dropzone_photo_delete(banner_id):
    banner = Banner.query.get_or_404(banner_id)
    if not banner:
        return jsonify({'error': '没有图片可以删除'}), 404

    file_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], banner.filename.split('/')[-1])
    if os.path.exists(file_path):
        os.remove(file_path)
    db.session.delete(banner)
    db.session.commit()

    return jsonify({'message': '删除成功'}), 200


@admin_bp.route('/intro_list', methods=['GET', 'POST'])  # 公司介绍列表
@login_required
def intro_list():
    intro = Introduce.query.all()
    return render_template('admin/introduce_list.html', intro=intro, show_intro_collapse=True)


@admin_bp.route('/intro_status/<int:intro_id>', methods=['GET', 'POST'])
@login_required
def intro_status(intro_id):
    intro = Introduce.query.get_or_404(intro_id)
    intro.status = not intro.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/intro_edit/<int:intro_id>', methods=['GET', 'POST'])  # 编辑公司介绍
@login_required
def intro_edit(intro_id):
    intro = Introduce.query.get_or_404(intro_id)
    form = EditIntroduceForm()
    if form.cancel.data:
        return redirect(url_for('admin.intro_list'))
    if form.validate_on_submit():
        intro.title = form.title.data
        intro.introduce_category_id = form.intro_category.data
        intro.introduce_content = form.intro_content.data
        intro.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.intro_list'))
    form.title.data = intro.title
    form.intro_category.data = intro.introduce_category_id
    form.intro_content.data = intro.introduce_content
    return render_template('admin/introduce_edit.html', intro=intro, form=form, show_intro_collapse=True)


@admin_bp.route('/intro_delete/<int:intro_id>', methods=['POST'])  # 删除公司介绍文章
@login_required
def intro_delete(intro_id):
    intro = Introduce.query.get_or_404(intro_id)
    db.session.delete(intro)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.intro_list'))


@admin_bp.route('/intro_multiple_delete', methods=['POST'])  # 批量删除文章
@login_required
def intro_multiple_delete():
    if request.method == 'POST':
        selected_ids = request.form.getlist('item_ids')
        for intro_id in selected_ids:
            intro = Introduce.query.get(intro_id)
            db.session.delete(intro)
        db.session.commit()
        flash('批量删除成功.', 'success')
        return redirect(url_for('admin.intro_list'))
    return redirect(url_for('admin.intro_list'))


@admin_bp.route('/intro/new', methods=['GET', 'POST'])  # 新建公司介绍文章
@login_required
def intro_add():
    form = IntroduceAddForm()
    if form.validate_on_submit():
        intro = Introduce(
            title=form.title.data,
            introduce_category_id=form.intro_category.data,
            introduce_content=form.intro_content.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(intro)
        db.session.commit()
        flash('添加成功.', 'success')
        return redirect(url_for('admin.intro_list'))
    return render_template('admin/introduce_add.html', form=form, show_collapse=True, show_intro_collapse=True)


@admin_bp.route('/intro_category_list', methods=['GET', 'POST'])  # 公司介绍分类
@login_required
def intro_category_list():
    intro_categories = IntroduceCategory.query.all()
    form = AddIntroCategoryForm()

    if form.validate_on_submit():
        intro_category = IntroduceCategory.query.filter_by(name=form.name.data.replace(' ', '')).first()
        if intro_category:
            flash('该介绍分类已经存在', 'warning')
            return redirect(url_for('admin.intro_category_list'))
        else:
            intro_category = IntroduceCategory(
                name=form.name.data,
                timestamp=datetime.utcnow()
            )
            db.session.add(intro_category)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.intro_category_list'))
    return render_template('admin/introduce_category_list.html', form=form, intro_categories=intro_categories,
                           show_intro_collapse=True)


@admin_bp.route('/intro_category_delete/<int:intro_category_id>', methods=['GET', 'POST'])  # 删除公司介绍分类
@login_required
def intro_category_delete(intro_category_id):
    intro_category = IntroduceCategory.query.get_or_404(intro_category_id)
    db.session.delete(intro_category)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.intro_category_list'))


@admin_bp.route('/intro_category_edit/<int:intro_category_id>', methods=['GET', 'POST'])  # 编辑公司介绍分类
@login_required
def intro_category_edit(intro_category_id):
    intro_category = IntroduceCategory.query.get_or_404(intro_category_id)
    form = EditIntroCategoryForm()
    if form.validate_on_submit():
        intro_category.name = form.name.data
        intro_category.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.intro_category_list'))
    form.name.data = intro_category.name
    return render_template('admin/introduce_category_edit.html', intro_category=intro_category, form=form,
                           show_intro_collapse=True)


@admin_bp.route('/intro_category_status/<int:intro_category_id>', methods=['GET', 'POST'])  # 公司介绍分类状态
@login_required
def intro_category_status(intro_category_id):
    intro_category = IntroduceCategory.query.get_or_404(intro_category_id)
    intro_category.status = not intro_category.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/research_list', methods=['GET', 'POST'])  # 研发生产文章列表
@login_required
def research_list():
    research = Research.query.all()
    return render_template('admin/research_list.html', research=research, show_research_collapse=True)


@admin_bp.route('/research_status/<int:research_id>', methods=['GET', 'POST'])  # 研发生产文章状态
@login_required
def research_status(research_id):
    research = Research.query.get_or_404(research_id)
    research.status = not research.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/research_edit/<int:research_id>', methods=['GET', 'POST'])  # 编辑研发生产文章
@login_required
def research_edit(research_id):
    research = Research.query.get_or_404(research_id)
    form = EditResearchForm()
    if form.cancel.data:
        return redirect(url_for('admin.research_list'))
    if form.validate_on_submit():
        research.title = form.title.data
        research.research_category_id = form.research_category.data
        research.research_content = form.research_content.data
        research.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.research_list'))
    form.title.data = research.title
    form.research_category.data = research.research_category_id
    form.research_content.data = research.research_content
    return render_template('admin/research_edit.html', research=research, form=form, show_research_collapse=True)


@admin_bp.route('/research_delete/<int:research_id>', methods=['POST'])  # 删除研发生产文章
@login_required
def research_delete(research_id):
    research = Research.query.get_or_404(research_id)
    db.session.delete(research)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.research_list'))


@admin_bp.route('/research_multiple_delete', methods=['POST'])  # 批量删除研发生产文章
@login_required
def research_multiple_delete():
    if request.method == 'POST':
        selected_ids = request.form.getlist('item_ids')
        for research_id in selected_ids:
            research = Research.query.get(research_id)
            db.session.delete(research)
        db.session.commit()
        flash('批量删除成功.', 'success')
        return redirect(url_for('admin.research_list'))
    return redirect(url_for('admin.research_list'))


@admin_bp.route('/research/new', methods=['GET', 'POST'])  # 新建研发生产文章
@login_required
def research_add():
    form = ResearchAddForm()
    if form.validate_on_submit():
        research = Research(
            title=form.title.data,
            research_category_id=form.research_category.data,
            research_content=form.research_content.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(research)
        db.session.commit()
        flash('添加成功.', 'success')
        return redirect(url_for('admin.research_list'))
    return render_template('admin/research_add.html', form=form, show_collapse=True, show_research_collapse=True)


@admin_bp.route('/research_category_list', methods=['GET', 'POST'])  # 研发生产分类
@login_required
def research_category_list():
    research_categories = ResearchCategory.query.all()
    form = AddIntroCategoryForm()

    if form.validate_on_submit():
        research_category = ResearchCategory.query.filter_by(name=form.name.data.replace(' ', '')).first()
        if research_category:
            flash('该介绍分类已经存在', 'warning')
            return redirect(url_for('admin.research_category_list'))
        else:
            research_category = ResearchCategory(
                name=form.name.data,
                timestamp=datetime.utcnow()
            )
            db.session.add(research_category)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.research_category_list'))
    return render_template('admin/research_category_list.html', form=form, research_categories=research_categories,
                           show_research_collapse=True)


@admin_bp.route('/research_category_delete/<int:research_category_id>', methods=['GET', 'POST'])  # 删除研发生产分类
@login_required
def research_category_delete(research_category_id):
    research_category = ResearchCategory.query.get_or_404(research_category_id)
    db.session.delete(research_category)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.research_category_list'))


@admin_bp.route('/research_category_edit/<int:research_category_id>', methods=['GET', 'POST'])  # 编辑研发生产分类
@login_required
def research_category_edit(research_category_id):
    research_category = ResearchCategory.query.get_or_404(research_category_id)
    form = EditIntroCategoryForm()
    if form.validate_on_submit():
        research_category.name = form.name.data
        research_category.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.research_category_list'))
    form.name.data = research_category.name
    return render_template('admin/research_category_edit.html', research_category=research_category, form=form,
                           show_research_collapse=True)


@admin_bp.route('/research_category_status/<int:research_category_id>', methods=['GET', 'POST'])  # 修改研发生产分类状态
@login_required
def research_category_status(research_category_id):
    research_category = ResearchCategory.query.get_or_404(research_category_id)
    research_category.status = not research_category.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/contact_list', methods=['GET', 'POST'])  # 研发生产文章列表
@login_required
def contact_list():
    contact = Contact.query.all()
    return render_template('admin/contact_list.html', contact=contact, show_contact_collapse=True)


@admin_bp.route('/contact_edit/<int:contact_id>', methods=['GET', 'POST'])  # 编辑联系我们文章
@login_required
def contact_edit(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    form = EditContactForm()
    if form.cancel.data:
        return redirect(url_for('admin.contact_list'))
    if form.validate_on_submit():
        contact.title = form.title.data
        contact.contact_category_id = form.contact_category.data
        contact.content = form.content.data
        contact.timestamp = datetime.utcnow()
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.contact_list'))
    form.title.data = contact.title
    form.contact_category.data = contact.contact_category_id
    form.content.data = contact.content
    return render_template('admin/contact_edit.html', contact=contact, form=form, show_contact_collapse=True)


@admin_bp.route('/contact_delete/<int:contact_id>', methods=['POST'])  # 删除联系我们文章
@login_required
def contact_delete(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.contact_list'))


@admin_bp.route('/contact_multiple_delete', methods=['POST'])  # 批量删除联系我们文章
@login_required
def contact_multiple_delete():
    if request.method == 'POST':
        selected_ids = request.form.getlist('item_ids')
        for contact_id in selected_ids:
            contact = Contact.query.get(contact_id)
            db.session.delete(contact)
        db.session.commit()
        flash('批量删除成功.', 'success')
        return redirect(url_for('admin.contact_list'))
    return redirect(url_for('admin.contact_list'))


@admin_bp.route('/contact/new', methods=['GET', 'POST'])  # 新建联系我们文章
@login_required
def contact_add():
    form = ContactAddForm()
    if form.validate_on_submit():
        contact = Contact(
            title=form.title.data,
            contact_category_id=form.contact_category.data,
            content=form.content.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(contact)
        db.session.commit()
        flash('添加成功.', 'success')
        return redirect(url_for('admin.contact_list'))
    return render_template('admin/contact_add.html', form=form, show_contact_collapse=True)


@admin_bp.route('/contact_category_list', methods=['GET', 'POST'])  # 联系我们分类
@login_required
def contact_category_list():
    contact_categories = ContactCategory.query.all()
    form = AddContactCategoryForm()

    if form.validate_on_submit():
        contact_category = ContactCategory.query.filter_by(name=form.name.data.replace(' ', '')).first()
        if contact_category:
            flash('该分类已经存在', 'warning')
            return redirect(url_for('admin.contact_category_list'))
        else:
            contact_category = ContactCategory(
                name=form.name.data,
            )
            db.session.add(contact_category)
            db.session.commit()
            flash('添加成功', 'success')
            return redirect(url_for('admin.contact_category_list'))
    return render_template('admin/contact_category_list.html', form=form, contact_categories=contact_categories,
                           show_contact_collapse=True)


@admin_bp.route('/contact_category_delete/<int:contact_category_id>', methods=['GET', 'POST'])  # 删除联系我们分类
@login_required
def contact_category_delete(contact_category_id):
    contact_category = ContactCategory.query.get_or_404(contact_category_id)
    db.session.delete(contact_category)
    db.session.commit()
    flash('删除成功.', 'success')
    return redirect(url_for('admin.contact_category_list'))


@admin_bp.route('/contact_category_edit/<int:contact_category_id>', methods=['GET', 'POST'])  # 编辑联系我们分类
@login_required
def contact_category_edit(contact_category_id):
    contact_category = ContactCategory.query.get_or_404(contact_category_id)
    form = EditContactCategoryForm()
    if form.validate_on_submit():
        contact_category.name = form.name.data
        db.session.commit()
        flash('修改成功.', 'success')
        return redirect(url_for('admin.contact_category_list'))
    form.name.data = contact_category.name
    return render_template('admin/contact_category_edit.html', contact_category=contact_category, form=form,
                           show_contact_collapse=True)


@admin_bp.route('/contact_status/<int:contact_id>', methods=['GET', 'POST'])  # 研发生产文章状态
@login_required
def contact_status(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    contact.status = not contact.status
    db.session.commit()
    return redirect_back()


@admin_bp.route('/index_about', methods=['GET', 'POST'])  # 首页简介
@login_required
def index_about():
    form = IndexAboutForm()
    if form.cancel.data:
        return redirect(url_for('admin.index_about'))
    if form.validate_on_submit():
        index_about = IndexAbout.query.first()
        if index_about:
            index_about.title = form.title.data
            index_about.content = form.content.data
            index_about.timestamp = datetime.utcnow()

            existing_images = index_about.filename if index_about.filename else []
            temp_files = request.form.get('temp_files')
            new_images = json.loads(temp_files) if temp_files else []
            updated_images = existing_images + new_images
            index_about.filename = updated_images

            db.session.commit()
            flash('修改成功.', 'success')
            return redirect(url_for('admin.index_about'))
        else:
            index_about = IndexAbout(
                title=form.title.data,
                content=form.content.data,
                ttimestamp=datetime.utcnow(),
                images=json.loads(request.form.get('temp_files')) if request.form.get('temp_files') else []
            )
            db.session.add(index_about)
            db.session.commit()
            flash('添加成功.', 'success')
            return redirect(url_for('admin.index_about'))
    index_about = IndexAbout.query.first()
    if index_about:
        form.title.data = index_about.title
        form.content.data = index_about.content
    return render_template('admin/index_about.html', form=form, index_about=index_about)


@admin_bp.route('/delete_uploaded_file', methods=['POST'])  # 删除上传的文件
@login_required
def delete_uploaded_file():
    data = request.get_json()
    print(data)
    required_fields = ['table_name', 'field_name', 'field_value']
    if not all(key in data for key in required_fields):
        return jsonify(success=False, message='缺少必要参数: table_name, field_name, field_value'), 400

    table_name = data['table_name']
    field_name = data['field_name']
    field_value = data['field_value']

    # 验证参数
    if not table_name or not field_name or not field_value:
        return jsonify(success=False, message='参数不能为空'), 400

    allowed_tables = {'indexabout', 'news', 'product'}
    if table_name not in allowed_tables:
        return jsonify(success=False, message='无效的表名'), 400

    try:
        # 动态获取模型类
        model_class = get_model_by_tablename(table_name)
        if not model_class:
            return jsonify(success=False, message='无效的表名'), 404

        # 验证字段是否存在
        if not hasattr(model_class, field_name):
            return jsonify(success=False, message='无效的字段名'), 400

        # 查询记录
        query_filter = {field_name: field_value}
        record = model_class.query.filter_by(**query_filter).first()
        if not record:
            return jsonify(success=False, message='记录不存在'), 404

        # 获取文件名并删除数据库记录
        filename = getattr(record, field_name)
        if isinstance(filename, list):
            # 处理字段存储的是 JSON 数组 ["img1.jpg", "img2.jpg"]
            if field_value not in filename:
                return jsonify(success=False, message='文件名不在记录中'), 400
            filename.remove(field_value)
            record.filename = json.dumps(filename)
        elif isinstance(filename, str):
            # 处理字段存储的是单个文件名
            if filename != field_value:
                return jsonify(success=False, message='文件名不匹配'), 400
            record.filename = None  # 或者其他默认值
        else:
            return jsonify(success=False, message='无效的文件名格式'), 400

        db.session.commit()

        # 删除服务器文件
        file_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], field_value)
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            current_app.logger.warning(f'文件不存在: {file_path}')

        return jsonify(success=True, message='文件删除成功')
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'文件删除失败: {e}')
        return jsonify(success=False, message=f'文件删除失败: {str(e)}'), 500


# 辅助函数：根据表名获取模型类
def get_model_by_tablename(table_name):
    # 获取所有已注册的模型类
    registry = db.Model.registry._class_registry
    for cls in registry.values():
        if hasattr(cls, '__table__') and cls.__table__.name == table_name:
            return cls
    return None



@admin_bp.route('/get_uploaded_files', methods=['GET'])
@login_required
def get_uploaded_files():
    """
    通用获取已上传文件列表
    参数说明（URL参数）：
    - model: 模型类名（如'News', 'Product'）
    - field: 存储文件名的字段（如'filename', 'images'）
    - filter_condition: 筛选条件（如'id=1'），可选
    """
    # 获取参数
    model_name = request.args.get('model')
    field_name = request.args.get('field')
    filter_condition = request.args.get('filter_condition', '')

    # 验证必要参数
    if not model_name or not field_name:
        raise BadRequest('Missing required parameters: model and field')

    # 动态获取模型类（安全考虑：限制允许访问的模型）
    allowed_models = {'IndexAbout', 'News', 'Product'}  # 允许访问的白名单
    if model_name not in allowed_models:
        raise BadRequest(f'Invalid model: {model_name}')

    model_class = getattr(models, model_name, None)
    if not model_class or not hasattr(model_class, field_name):
        raise BadRequest('Invalid model or field')

    # 获取上传目录
    upload_folder = current_app.config['BQ_UPLOAD_PATH']
    if not os.path.exists(upload_folder):
        return jsonify(files=[])

    # 构建查询
    try:
        query = model_class.query
        # 处理过滤条件（示例：id=1 -> filter_by(id=1)）
        if filter_condition:
            key, value = filter_condition.split('=', 1)
            query = query.filter_by(**{key.strip(): value.strip()})

        records = query.all()
    except Exception as e:
        current_app.logger.error(f"Database query failed: {str(e)}")
        return jsonify(files=[])

    # 提取文件名（处理不同存储格式）
    all_filenames = []
    for record in records:
        field_value = getattr(record, field_name)
        if not field_value:
            continue
        # 处理不同存储格式：字符串、JSON数组、逗号分隔等
        if isinstance(field_value, list):
            all_filenames.extend(field_value)
        elif field_value.startswith('['):  # 假设是JSON数组
            try:
                all_filenames.extend(json.loads(field_value))
            except json.JSONDecodeError:
                continue
        else:
            all_filenames.append(field_value)

    # 验证文件存在性
    existing_files = []
    for f in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, f)
        if os.path.isfile(file_path) and f in all_filenames:
            existing_files.append(f)

    return jsonify(files=existing_files)


# 类型与数据表的映射
MODEL_MAP = {
    'category-input': Category,
    'brand-input': Brand,
    'subject-input': Subject,
    'news-category-input': NewsCategory,
    'intro-category-input': IntroduceCategory,
    'research-category-input': ResearchCategory,
    'contact-category-input': ContactCategory,
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

@admin_bp.route('/routes')
def list_routes():
    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        line = f"{rule.endpoint}: {rule.rule} [{methods}]"
        output.append(line)
    return '<br>'.join(output)
