from flask import render_template, request, redirect, url_for, Blueprint, current_app, flash, send_from_directory
from bqwebsite.models import Category, Product, News, Brand, Honor, Banner, Introduce, Photo, NewsCategory, \
    IntroduceCategory, Contact, ContactCategory, Subject

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
# 主页
def index():
    return render_template('main/index.html')


@main_bp.route('/news-category/<int:news_category_id>')
# 新闻分类页面
def show_news_category(news_category_id):
    news_category = NewsCategory.query.get_or_404(news_category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_NEWS_PER_PAGE']
    pagination = News.query.with_parent(news_category).order_by(News.timestamp.desc()).paginate(page=page,
                                                                                                per_page=per_page)
    news_list = pagination.items

    return render_template('main/news_category.html', news_category=news_category, news_list=news_list,
                           pagination=pagination)


@main_bp.route('/news/<int:news_id>')
# 新闻详细页面
def show_news(news_id):
    news_detail = News.query.get_or_404(news_id)
    return render_template('main/news_detail.html', news_detail=news_detail)


@main_bp.route('/news/n/<int:news_id>')
# 下一篇文章
def news_next(news_id):
    news_n_detail = News.query.get_or_404(news_id)
    news_n = News.query.with_parent(news_n_detail.newscategory).filter(News.timestamp < news_n_detail.timestamp).order_by(News.timestamp.desc()).first()

    if news_n is None:
        flash('已经是最后一篇文章', 'info')
        return redirect(url_for('main.show_news', news_id=news_id))
    return redirect(url_for('main.show_news', news_id=news_n.id))

@main_bp.route('/news/p/<int:news_id>')
# 上一篇文章
def news_previous(news_id):
    news_p_detail = News.query.get_or_404(news_id)
    news_p = News.query.with_parent(news_p_detail.newscategory).filter(News.timestamp > news_p_detail.timestamp).order_by(News.timestamp.asc()).first()

    if news_p is None:
        flash('已经是最新一篇文章', 'info')
        return redirect(url_for('main.show_news', news_id=news_id))
    return redirect(url_for('main.show_news', news_id=news_p.id))

@main_bp.route('/news')
# 全部新闻页面
def news():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_NEWS_PER_PAGE']
    pagination = News.query.order_by(News.timestamp.desc()).paginate(page=page, per_page=per_page)
    all_news = pagination.items
    return render_template('main/news.html', all_news=all_news, pagination=pagination)


@main_bp.route('/products')  # 所有产品
def product():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.filter(Product.status == True).order_by(Product.timestamp.desc()).paginate(page=page, per_page=per_page)
    products = pagination.items
    return render_template('main/products.html', products=products, pagination=pagination)


@main_bp.route('/category/<category>')  # 按剂型分类
def product_category(category):
    category = Category.query.filter_by(name=category).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.with_parent(category).order_by(Product.timestamp.desc()).paginate(page=page, per_page=per_page)
    products = pagination.items
    return render_template('main/product_category.html', category=category, pagination=pagination, products=products)

@main_bp.route('/brand/<brand>')  # 按商标分类
def product_brand(brand):
    brand = Brand.query.filter_by(name=brand).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.with_parent(brand).order_by(Product.timestamp.desc()).paginate(page=page, per_page=per_page)
    products = pagination.items
    return render_template('main/product_brand.html', brand=brand, pagination=pagination, products=products)


@main_bp.route('/subject/<subject>')  # 按功能主治分类
def product_subject(subject):
    subject = Subject.query.filter_by(name=subject).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BQ_PRODUCT_PER_PAGE']
    pagination = Product.query.with_parent(subject).order_by(Product.timestamp.desc()).paginate(page=page, per_page=per_page)
    products = pagination.items
    return render_template('main/product_subject.html', subject=subject, pagination=pagination, products=products)


@main_bp.route('/products/n/<int:product_id>')
# 下一个品种
def product_next(product_id):
    product_n_detail = Product.query.get_or_404(product_id)
    product_n = Product.query.with_parent(product_n_detail.category).filter(Product.timestamp < product_n_detail.timestamp).order_by(Product.timestamp.desc()).first()

    if product_n is None:
        flash('已经是第一个', 'info')
        return redirect(url_for('main.show_product', product_id=product_id))
    return redirect(url_for('main.show_product', product_id=product_n.id))

@main_bp.route('/product/p/<int:product_id>')
# 上一个品种
def product_previous(product_id):
    product_p_detail = Product.query.get_or_404(product_id)
    product_p = Product.query.with_parent(product_p_detail.category).filter(Product.timestamp > product_p_detail.timestamp).order_by(Product.timestamp.asc()).first()

    if product_p is None:
        flash('已经是最后一个', 'info')
        return redirect(url_for('main.show_product', product_id=product_id))
    return redirect(url_for('main.show_product', product_id=product_p.id))


@main_bp.route('/product_detail/<int:product_id>')  # 产品详细页面
def show_product(product_id):
    product = Product.query.get_or_404(product_id)
    # 获取上一个品种
    product_p = Product.query.with_parent(product.category).filter(Product.timestamp < product.timestamp).order_by(Product.timestamp.desc()).first()
    # 获取下一个品种
    product_n = Product.query.with_parent(product.category).filter(Product.timestamp > product.timestamp).order_by(Product.timestamp.asc()).first()
    return render_template('main/product_detail.html', product=product, product_p=product_p, product_n=product_n)


# @main_bp.route('/introduce-category/<int:intro_category_id>')
# def show_introduce_category(intro_category_id):
#     intro_category = IntroduceCategory.query.get_or_404(intro_category_id)
#     return render_template('main/introduce_detail.html', intro_category=intro_category)


@main_bp.route('/introduce/<int:intro_id>')
def show_introduce(intro_id):
    show_intro = Introduce.query.get_or_404(intro_id)
    return render_template('main/introduce_detail.html', show_intro=show_intro)


@main_bp.route('/honor')
def honor():
    return render_template('main/honor.html')


@main_bp.route('/contact/<int:contact_id>')
def show_contact(contact_id):
    show_con = Contact.query.get_or_404(contact_id)
    return render_template('main/contact_detail.html', show_con=show_con)


@main_bp.route('/contact_cooperate')
def contact_cooperate():
    return render_template('main/contact_cooperate.html')


@main_bp.route('/contact_recruit')
def contact_recruit():
    return render_template('main/contact_recruit.html')

@main_bp.route('/uploads/<int:filename>')  # 获得图片链接
def get_image(filename):
    return send_from_directory(current_app.config['BQ_UPLOAD_PATH'], filename)
