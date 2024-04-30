from flask import render_template, request, redirect, url_for, Blueprint, current_app
from bqwebsite.models import Category, Product, News, Brand, Honor, Banner, Introduce, Photo, NewsCategory, IntroduceCategory


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/news-category/<int:news_category_id>')
def show_news_category(news_category_id):
    news_category = NewsCategory.query.get_or_404(news_category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_NEWS_PER_PAGE']
    pagination = News.query.with_parent(news_category).order_by(News.timestamp.desc()).paginate(page=page, per_page=per_page)
    news_list = pagination.items

    return render_template('main/news_category.html', news_category=news_category, news_list=news_list, pagination=pagination)

@main_bp.route('/news/<int:news_id>')
def show_news(news_id):
    news_content = News.query.get_or_404(news_id)
    return render_template('main/news_detail.html', news_content=news_content)

@main_bp.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_NEWS_PER_PAGE']
    pagination = News.query.order_by(News.timestamp.desc()).paginate(page=page, per_page=per_page)
    all_news = pagination.items
    return render_template('main/news.html', all_news=all_news, pagination=pagination)

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
