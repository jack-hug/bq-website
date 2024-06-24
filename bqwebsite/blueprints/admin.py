from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import current_user, login_user, login_required, logout_user

from bqwebsite.models import Admin
from bqwebsite.forms.admin import LoginForm

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def index():
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
    return render_template('admin/upload.html')


@admin_bp.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    return render_template('admin/reset_password.html')
