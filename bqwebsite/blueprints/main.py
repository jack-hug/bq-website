from flask import render_template, request, redirect, url_for, Blueprint
from bqwebsite.models import Category, Product, New, Brand, Honor, Banner, Introduce, Photo, NewCategory, IntroduceCategory


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/news')
def news():
    return render_template('main/news.html')


@main_bp.route('/news_company')
def news_company():
    return render_template('main/news_company.html')


@main_bp.route('/news_industry')
def news_industry():
    return render_template('main/news_industry.html')


@main_bp.route('/news_file')
def news_file():
    return render_template('main/news_file.html')


@main_bp.route('/news_detail')
def news_detail():
    return render_template('main/news_detail.html')


@main_bp.route('/product')
def product():
    return render_template('main/product.html')

@main_bp.route('/product_categories')
def product_categories():
    return render_template('main/product_categories.html')

@main_bp.route('/product_detail')
def product_detail():
    return render_template('main/product_detail.html')


@main_bp.route('/introduce')
def introduce():
    return render_template('main/introduce.html')


@main_bp.route('/introduce_company')
def introduce_company():
    return render_template('main/introduce_company.html')


@main_bp.route('/introduce_quality')
def introduce_quality():
    return render_template('main/introduce_quality.html')


@main_bp.route('/introduce_structure')
def introduce_structure():
    return render_template('main/introduce_structure.html')


@main_bp.route('/introduce_responsibility')
def introduce_responsibility():
    return render_template('main/introduce_responsibility.html')


@main_bp.route('/honor')
def honor():
    return render_template('main/honor.html')


@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')


@main_bp.route('/contact_cooperate')
def contact_cooperate():
    return render_template('main/contact_cooperate.html')


@main_bp.route('/contact_recruit')
def contact_recruit():
    return render_template('main/contact_recruit.html')
