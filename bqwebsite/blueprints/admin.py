import os.path

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import current_user, login_user, login_required, logout_user

from bqwebsite.extensions import db
from bqwebsite.models import Admin, Photo, Product, Brand, Category, Subject, News, NewsCategory
from bqwebsite.forms.admin import LoginForm
from bqwebsite.utils import random_filename, resize_image

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template('admin/index.html')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('Login success...', 'info')
                return redirect(url_for('admin.index'))
        flash('Invalid email or password.', 'warning')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('main.index'))


@admin_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')
        filename = random_filename(f.filename)
        f.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
        filename_s = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('admin/upload.html')


@admin_bp.route('/uploads/<int:filename>')
@login_required
def get_image(filename):
    return send_from_directory(current_app.config['BQ_UPLOAD_PATH'], filename)


@admin_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    return render_template('admin/reset_password.html')


@admin_bp.route('/product_list', methods=['GET', 'POST'])
@login_required
def product_list():
    products_length = Product.query.count()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.order_by(Product.id.asc()).paginate(page=page, per_page=per_page)
    products = pagination.items
    return render_template('admin/product_list.html', products=products, pagination=pagination, products_length=products_length)

@admin_bp.route('/category_list', methods=['GET', 'POST'])
@login_required
def category_list():
    return render_template('admin/category_list.html')

@admin_bp.route('/brand_edit/<int:brand_id>', methods=['GET', 'POST'])
@login_required
def brand_edit(brand_id):
    brand_id = Brand.query.get_or_404(brand_id)
    return render_template('admin/category_edit.html', brand_id=brand_id)

@admin_bp.route('/category_edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def category_edit(category_id):
    category_id = Category.query.get_or_404(category_id)
    return render_template('admin/category_edit.html', category_id=category_id)

@admin_bp.route('/subject_edit/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def subject_edit(subject_id):
    subject_id = Subject.query.get_or_404(subject_id)
    return render_template('admin/category_edit.html', subject_id=subject_id)

@admin_bp.route('/news_list', methods=['GET', 'POST'])
@login_required
def news_list():
    news_length = News.query.count()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = News.query.order_by(News.id.asc()).paginate(page=page, per_page=per_page)
    news = pagination.items
    return render_template('admin/news_list.html', news=news, pagination=pagination, news_length=news_length)

@admin_bp.route('/news_category_list', methods=['GET', 'POST'])
@login_required
def news_category_list():
    return render_template('admin/news_category_list.html')

@admin_bp.route('/news_edit/<int:news_id>', methods=['GET', 'POST'])
@login_required
def news_edit(news_id):
    news_id = News.query.get_or_404(news_id)
    return render_template('admin/category_edit.html', news_id=news_id)

@admin_bp.route('/news_category_edit/<int:news_category_id>', methods=['GET', 'POST'])
@login_required
def news_category_edit(news_category_id):
    news_category_id = NewsCategory.query.get_or_404(news_category_id)
    return render_template('admin/category_edit.html', news_category_id=news_category_id)
