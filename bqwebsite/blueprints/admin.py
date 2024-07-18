import os.path

from flask import render_template, Blueprint, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import current_user, login_user, login_required, logout_user

from bqwebsite.extensions import db
from bqwebsite.models import Admin, Photo
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
def get_image(filename):
    return send_from_directory(current_app.config['BQ_UPLOAD_PATH'], filename)


@admin_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    return render_template('admin/reset_password.html')
