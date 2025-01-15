import os

from flask import render_template, request, redirect, url_for, Blueprint, current_app, flash, send_from_directory, \
    jsonify
from sqlalchemy.orm import joinedload, contains_eager

from ..models import Category, Product, News, Brand, Honor, Banner, Introduce, Photo, NewsCategory, \
    IntroduceCategory, Contact, ContactCategory, Subject, Research, ResearchCategory

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
# 主页
def index():
    return render_template('main/index.html')


@main_bp.route('/news-category/<int:news_category_id>')
# 新闻分类页面
def show_news_category(news_category_id):
    news_category = NewsCategory.query.get_or_404(news_category_id)
    if not news_category.status:
        flash('该新闻分类不存在', 'info')
        return redirect(url_for('main.news'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_NEWS_PER_PAGE']
    pagination = News.query.with_parent(news_category).filter(News.status == True).order_by(
        News.timestamp.desc()).paginate(page=page,
                                        per_page=per_page)
    news_list = pagination.items

    return render_template('main/news_category.html', news_category=news_category, news_list=news_list,
                           pagination=pagination)


@main_bp.route('/news/<int:news_id>')
# 新闻详细页面
def show_news(news_id):
    news_detail = News.query.get_or_404(news_id)
    if not news_detail.status:
        flash('该新闻不存在', 'info')
        return redirect(url_for('main.news'))
    return render_template('main/news_detail.html', news_detail=news_detail)


@main_bp.route('/news/n/<int:news_id>')
# 下一篇文章
def news_next(news_id):
    news_n_detail = News.query.get_or_404(news_id)
    if not news_n_detail.status:
        flash('该文章不存在', 'info')
        return redirect(url_for('main.show_news', news_id=news_id))
    news_n = News.query.with_parent(news_n_detail.newscategory).filter(
        News.timestamp < news_n_detail.timestamp, News.status == True).order_by(News.timestamp.desc()).first()

    if news_n is None:
        flash('已经是最后一篇文章', 'info')
        return redirect(url_for('main.show_news', news_id=news_id))
    return redirect(url_for('main.show_news', news_id=news_n.id))


@main_bp.route('/news/p/<int:news_id>')
# 上一篇文章
def news_previous(news_id):
    news_p_detail = News.query.get_or_404(news_id)
    if not news_p_detail.status:
        flash('该文章不存在', 'info')
        return redirect(url_for('main.show_news', news_id=news_id))
    news_p = News.query.with_parent(news_p_detail.newscategory).filter(
        News.timestamp > news_p_detail.timestamp, News.status == True).order_by(News.timestamp.asc()).first()

    if news_p is None:
        flash('已经是最新一篇文章', 'info')
        return redirect(url_for('main.show_news', news_id=news_id))
    return redirect(url_for('main.show_news', news_id=news_p.id))


@main_bp.route('/news')
# 全部新闻页面
def news():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_NEWS_PER_PAGE']
    pagination = News.query.filter(News.status == True).order_by(News.timestamp.desc()).paginate(page=page,
                                                                                                 per_page=per_page)
    all_news = pagination.items
    return render_template('main/news.html', all_news=all_news, pagination=pagination)


@main_bp.route('/products')  # 所有产品
def product():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.filter(Product.status == True).order_by(Product.timestamp.desc()).paginate(page=page,
                                                                                                          per_page=per_page)
    products = pagination.items
    return render_template('main/products.html', products=products, pagination=pagination)


@main_bp.route('/category/<category>')  # 按剂型分类
def product_category(category):
    category = Category.query.filter_by(name=category).first_or_404()
    if not category.status:
        flash('该分类不存在', 'info')
        return redirect(url_for('main.product'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.with_parent(category).filter(Product.status == True).order_by(
        Product.timestamp.desc()).paginate(page=page,
                                           per_page=per_page)
    products = pagination.items
    return render_template('main/product_category.html', category=category, pagination=pagination, products=products)


@main_bp.route('/brand/<brand>')  # 按商标分类
def product_brand(brand):
    brand = Brand.query.filter_by(name=brand).first_or_404()
    if not brand.status:
        flash('该商标不存在', 'info')
        return redirect(url_for('main.product'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.with_parent(brand).filter(Product.status == True).order_by(
        Product.timestamp.desc()).paginate(page=page,
                                           per_page=per_page)
    products = pagination.items
    return render_template('main/product_brand.html', brand=brand, pagination=pagination, products=products)


@main_bp.route('/subject/<subject>')  # 按功能主治分类
def product_subject(subject):
    subject = Subject.query.filter_by(name=subject).first_or_404()
    if not subject.status:
        flash('该功能主治不存在', 'info')
        return redirect(url_for('main.product'))
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.with_parent(subject).filter(Product.status == True).order_by(
        Product.timestamp.desc()).paginate(page=page,
                                           per_page=per_page)
    products = pagination.items
    return render_template('main/product_subject.html', subject=subject, pagination=pagination, products=products)


@main_bp.route('/products/n/<int:product_id>')
# 下一个品种
def product_next(product_id):
    product_n_detail = Product.query.get_or_404(product_id)
    if not product_n_detail.status:
        flash('该品种不存在', 'info')
        return redirect(url_for('main.product'))
    product_n = Product.query.with_parent(product_n_detail.category).filter(
        Product.timestamp > product_n_detail.timestamp).order_by(Product.timestamp.asc()).first()

    if product_n is None:
        flash('已经是一个', 'info')
        return redirect(url_for('main.show_product', product_id=product_id))
    return redirect(url_for('main.show_product', product_id=product_n.id))


@main_bp.route('/products/p/<int:product_id>')
# 上一个品种
def product_previous(product_id):
    product_p_detail = Product.query.get_or_404(product_id)
    if not product_p_detail.status:
        flash('该品种不存在', 'info')
        return redirect(url_for('main.product'))
    product_p = Product.query.with_parent(product_p_detail.category).filter(
        Product.timestamp < product_p_detail.timestamp).order_by(Product.timestamp.desc()).first()

    if product_p is None:
        flash('已经是最后一个', 'info')
        return redirect(url_for('main.show_product', product_id=product_id))
    return redirect(url_for('main.show_product', product_id=product_p.id))


@main_bp.route('/product_detail/<int:product_id>')  # 产品详细页面
def show_product(product_id):
    product = Product.query.get_or_404(product_id)
    if not product.status:
        flash('该产品不存在', 'info')
        return redirect(url_for('main.product'))

    # 获取上一个品种
    product_p = Product.query.with_parent(product.category).filter(Product.timestamp < product.timestamp,
                                                                   Product.status == True).order_by(
        Product.timestamp.desc()).first()
    product_p_name = product_p.name if product_p else None
    # 获取下一个品种
    product_n = Product.query.with_parent(product.category).filter(Product.timestamp > product.timestamp,
                                                                   Product.status == True).order_by(
        Product.timestamp.asc()).first()
    product_n_name = product_n.name if product_n else None
    return render_template('main/product_detail.html', product=product, product_p_name=product_p_name,
                           product_n_name=product_n_name)


@main_bp.route('/introduce/<int:intro_id>')
# 公司介绍
def show_intro(intro_id):
    intro_categories = (
        IntroduceCategory.query
        .join(IntroduceCategory.introduces)  # 关联 Introduce 表
        .filter(Introduce.status == True)  # 筛选 status 为 True 的记录
        .options(contains_eager(IntroduceCategory.introduces))  # 预加载 introduces 数据
        .order_by(IntroduceCategory.id.asc())
        .all()
    )
    intro = Introduce.query.filter_by(id=intro_id, status=True).first_or_404()
    if not intro.status or not intro.introduce_category.status:
        flash('该介绍不存在', 'warning')
        return redirect(url_for('main.index'))
    return render_template('main/introduce_detail.html', intro=intro, intro_categories=intro_categories)


@main_bp.route('/honor')
# 荣誉介绍
def honor():
    return render_template('main/honor.html')


@main_bp.route('/contact/<int:contact_id>')
# 联系我们
def show_contact(contact_id):
    show_contact = Contact.query.get_or_404(contact_id)
    if contact_id == 2:
        template_name = 'main/contact_cooperation.html'
    else:
        template_name = 'main/contact_detail.html'
    return render_template(template_name, show_contact=show_contact)


@main_bp.route('/research/<int:research_id>')
# 研发生产
def show_research(research_id):
    research_categories = (
        ResearchCategory.query
        .join(ResearchCategory.researchs)
        .filter(Research.status == True)
        .options(contains_eager(ResearchCategory.researchs))
        .order_by(ResearchCategory.id.asc())
        .all()
    )
    research = Research.query.filter_by(id=research_id, status=True).first_or_404()
    return render_template('main/research_detail.html', research=research, research_categories=research_categories)


@main_bp.route('/uploads/<int:filename>')  # 获得图片链接
def get_image(filename):
    return send_from_directory(current_app.config['BQ_UPLOAD_PATH'], filename)
