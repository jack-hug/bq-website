[1mdiff --git a/bqwebsite/__init__.py b/bqwebsite/__init__.py[m
[1mindex 836f002..74d0098 100644[m
[1m--- a/bqwebsite/__init__.py[m
[1m+++ b/bqwebsite/__init__.py[m
[36m@@ -1,201 +1,201 @@[m
[31m-import click[m
[31m-import os[m
[31m-[m
[31m-from flask import Flask, render_template, jsonify[m
[31m-from flask_wtf.csrf import CSRFError[m
[31m-from sqlalchemy import or_[m
[31m-from sqlalchemy.orm import contains_eager[m
[31m-[m
[31m-from .blueprints.main import main_bp[m
[31m-from .blueprints.admin import admin_bp[m
[31m-from .config import config[m
[31m-from .extensions import bootstrap, db, csrf, login_manager, ckeditor, migrate, moment[m
[31m-from .models import Category, Product, News, Brand, Honor, Banner, Introduce, Photo, NewsCategory, \[m
[31m-    IntroduceCategory, Admin, Subject, ContactCategory, ResearchCategory, Research, Contact[m
[31m-from .utils import clean_temp_folder[m
[31m-[m
[31m-[m
[31m-def create_app(config_name=None):[m
[31m-    if config_name is None:[m
[31m-        config_name = os.getenv('FLASK_CONFIG', 'development')[m
[31m-[m
[31m-    app = Flask('bqwebsite')[m
[31m-[m
[31m-    app.config.from_object(config[config_name])[m
[31m-[m
[31m-    register_extensions(app)[m
[31m-    register_blueprints(app)[m
[31m-    register_shell_context(app)[m
[31m-    register_errorhandlers(app)[m
[31m-    register_commands(app)[m
[31m-    register_template_context(app)[m
[31m-[m
[31m-    with app.app_context():[m
[31m-        clean_temp_folder()[m
[31m-[m
[31m-    return app[m
[31m-[m
[31m-[m
[31m-def register_extensions(app):[m
[31m-    bootstrap.init_app(app)[m
[31m-    db.init_app(app)[m
[31m-    csrf.init_app(app)[m
[31m-    login_manager.init_app(app)[m
[31m-    ckeditor.init_app(app)[m
[31m-    migrate.init_app(app, db)[m
[31m-    moment.init_app(app)[m
[31m-[m
[31m-[m
[31m-def register_blueprints(app):[m
[31m-    app.register_blueprint(main_bp)[m
[31m-    app.register_blueprint(admin_bp, url_prefix='/admin')[m
[31m-[m
[31m-[m
[31m-def register_template_context(app):[m
[31m-    @app.context_processor[m
[31m-    def make_template_context():[m
[31m-        admin = Admin.query.first()[m
[31m-        categories = Category.query.order_by(Category.id.asc()).all()[m
[31m-        subjects = Subject.query.order_by(Subject.id.asc()).all()[m
[31m-        brands = Brand.query.order_by(Brand.id.asc()).all()[m
[31m-        all_news_limit = News.query.filter(News.status == True).order_by(News.clicks.desc()).limit(10).all()[m
[31m-        news_categories = NewsCategory.query.filter(NewsCategory.status == True).order_by(NewsCategory.id.asc()).all()[m
[31m-        intro_categories = ([m
[31m-            IntroduceCategory.query[m
[31m-            .join(IntroduceCategory.introduces)[m
[31m-            .filter(Introduce.status == True)[m
[31m-            .options(contains_eager(IntroduceCategory.introduces))[m
[31m-            .order_by(IntroduceCategory.id.asc())[m
[31m-            .all()[m
[31m-        )[m
[31m-        research_categories = ([m
[31m-            ResearchCategory.query[m
[31m-            .join(ResearchCategory.researchs)[m
[31m-            .filter(Research.status == True)[m
[31m-            .options(contains_eager(ResearchCategory.researchs))[m
[31m-            .order_by(ResearchCategory.id.asc())[m
[31m-            .all()[m
[31m-        )[m
[31m-        contact_categories = ([m
[31m-            ContactCategory.query[m
[31m-            .join(ContactCategory.contacts)[m
[31m-            .filter(Contact.status == True)[m
[31m-            .options(contains_eager(ContactCategory.contacts))[m
[31m-            .order_by(ContactCategory.id.asc())[m
[31m-            .all()[m
[31m-        )[m
[31m-        hot_products = Product.query.filter(Product.clicks > 0, Product.status == True).order_by([m
[31m-            Product.clicks.desc()).limit(15)[m
[31m-        return dict(admin=admin, categories=categories, subjects=subjects, brands=brands,[m
[31m-                    news_categories=news_categories, contact_categories=contact_categories,[m
[31m-                    all_news_limit=all_news_limit, hot_products=hot_products,intro_categories=intro_categories,[m
[31m-                    research_categories=research_categories)[m
[31m-[m
[31m-[m
[31m-def register_shell_context(app):[m
[31m-    @app.shell_context_processor[m
[31m-    def make_shell_context():[m
[31m-        return dict(db=db)[m
[31m-[m
[31m-[m
[31m-def register_errorhandlers(app):[m
[31m-    @app.errorhandler(400)[m
[31m-    def bad_request(e):[m
[31m-        return render_template('errors/400.html'), 400[m
[31m-[m
[31m-    @app.errorhandler(403)[m
[31m-    def forbidden(e):[m
[31m-        return render_template('errors/403.html'), 403[m
[31m-[m
[31m-    @app.errorhandler(404)[m
[31m-    def page_not_found(e):[m
[31m-        return render_template('errors/404.html'), 404[m
[31m-[m
[31m-    @app.errorhandler(413)[m
[31m-    def request_entity_too_large(e):[m
[31m-        return render_template('errors/413.html'), 413[m
[31m-[m
[31m-    @app.errorhandler(500)[m
[31m-    def internal_server_error(e):[m
[31m-        return render_template('errors/500.html'), 500[m
[31m-[m
[31m-    @app.errorhandler(CSRFError)[m
[31m-    def handle_csrf_error(e):[m
[31m-        return render_template('errors/400.html', description=e.description), 400[m
[31m-[m
[31m-[m
[31m-def register_commands(app):[m
[31m-    @app.cli.command()[m
[31m-    @click.option('--drop', is_flag=True, help='Create after drop.')[m
[31m-    def initdb(drop):[m
[31m-        if drop:[m
[31m-            click.confirm('This operation will delete the database, do you want to continue?', abort=True)[m
[31m-            db.drop_all()[m
[31m-            click.echo('Drop tables...')[m
[31m-        db.create_all()[m
[31m-        click.echo('Initialized database...')[m
[31m-        Category.get_default_category()[m
[31m-        Brand.get_default_brand()[m
[31m-        Subject.get_default_subject()[m
[31m-        click.echo('Initialized default category, Brand, Subject...')[m
[31m-[m
[31m-    @app.cli.command()[m
[31m-    @click.option('--product', default=30, help='Quantity of products, default is 30.')[m
[31m-    @click.option('--news', default=30, help='Quantity of products, default is 30.')[m
[31m-    @click.option('--introduce', default=5, help='Quantity of introduce, default is 5.')[m
[31m-    @click.option('--research', default=3, help='Quantity of research and development, default is 3.')[m
[31m-    @click.option('--contact', default=3, help='Quantity of contact, default is 3.')[m
[31m-    @click.option('--photo', default=50, help='Quantity of photos, default is 50.')[m
[31m-    def forge(product, news, introduce, contact, photo, research):[m
[31m-        from .fakes import fake_categories, admin, fake_products, news_categories, fake_news, intro_category, \[m
[31m-            fake_intro, fake_brand, fake_subject, contact_categories, fake_contact, fake_photo, research_category, \[m
[31m-            fake_research, fake_index_about, fake_banners[m
[31m-[m
[31m-        click.echo('Drop tables....')[m
[31m-        db.drop_all()[m
[31m-        click.echo('Initialized database......')[m
[31m-        db.create_all()[m
[31m-        Category.get_default_category()[m
[31m-        Brand.get_default_brand()[m
[31m-        Subject.get_default_subject()[m
[31m-        click.echo('Generating default category, Brand, Subject...')[m
[31m-[m
[31m-        click.echo('Generating the administrator...')[m
[31m-        admin()[m
[31m-[m
[31m-        click.echo('Generating product_categories...')[m
[31m-        fake_categories()[m
[31m-[m
[31m-        click.echo('Generating brand and subject...')[m
[31m-        fake_brand()[m
[31m-        fake_subject()[m
[31m-[m
[31m-        click.echo('Generating %d products...' % product)[m
[31m-        fake_products(product)[m
[31m-[m
[31m-        click.echo('Generating %d photos...' % photo)[m
[31m-        fake_photo(photo)[m
[31m-[m
[31m-        click.echo('Generating news_categories and %d news...' % news)[m
[31m-        news_categories()[m
[31m-        fake_news(news)[m
[31m-[m
[31m-        click.echo('Generating research_categories and %d research contents...' % research)[m
[31m-        research_category()[m
[31m-        fake_research(research)[m
[31m-[m
[31m-        click.echo('Generating contact_category and %d contact' % contact)[m
[31m-        contact_categories()[m
[31m-        fake_contact(contact)[m
[31m-[m
[31m-        click.echo('Generating intro_categories and %d introduce...' % introduce)[m
[31m-        intro_category()[m
[31m-        fake_intro(introduce)[m
[31m-[m
[31m-        click.echo('Generating index_about...')[m
[31m-        fake_index_about()[m
[31m-[m
[31m-        click.echo('Generating banner photos...')[m
[31m-        fake_banners()[m
[31m-[m
[31m-        click.echo('Done!')[m
[32m+[m[32mimport click[m[41m[m
[32m+[m[32mimport os[m[41m[m
[32m+[m[41m[m
[32m+[m[32mfrom flask import Flask, render_template, jsonify[m[41m[m
[32m+[m[32mfrom flask_wtf.csrf import CSRFError[m[41m[m
[32m+[m[32mfrom sqlalchemy import or_[m[41m[m
[32m+[m[32mfrom sqlalchemy.orm import contains_eager[m[41m[m
[32m+[m[41m[m
[32m+[m[32mfrom .blueprints.main import main_bp[m[41m[m
[32m+[m[32mfrom .blueprints.admin import admin_bp[m[41m[m
[32m+[m[32mfrom .config import config[m[41m[m
[32m+[m[32mfrom .extensions import bootstrap, db, csrf, login_manager, ckeditor, migrate, moment[m[41m[m
[32m+[m[32mfrom .models import Category, Product, News, Brand, Honor, Banner, Introduce, Photo, NewsCategory, \[m[41m[m
[32m+[m[32m    IntroduceCategory, Admin, Subject, ContactCategory, ResearchCategory, Research, Contact[m[41m[m
[32m+[m[32mfrom .utils import clean_temp_folder[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
[32m+[m[32mdef create_app(config_name=None):[m[41m[m
[32m+[m[32m    if config_name is None:[m[41m[m
[32m+[m[32m        config_name = os.getenv('FLASK_CONFIG', 'development')[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    app = Flask('bqwebsite')[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    app.config.from_object(config[config_name])[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    register_extensions(app)[m[41m[m
[32m+[m[32m    register_blueprints(app)[m[41m[m
[32m+[m[32m    register_shell_context(app)[m[41m[m
[32m+[m[32m    register_errorhandlers(app)[m[41m[m
[32m+[m[32m    register_commands(app)[m[41m[m
[32m+[m[32m    register_template_context(app)[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    with app.app_context():[m[41m[m
[32m+[m[32m        clean_temp_folder()[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    return app[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
[32m+[m[32mdef register_extensions(app):[m[41m[m
[32m+[m[32m    bootstrap.init_app(app)[m[41m[m
[32m+[m[32m    db.init_app(app)[m[41m[m
[32m+[m[32m    csrf.init_app(app)[m[41m[m
[32m+[m[32m    login_manager.init_app(app)[m[41m[m
[32m+[m[32m    ckeditor.init_app(app)[m[41m[m
[32m+[m[32m    migrate.init_app(app, db)[m[41m[m
[32m+[m[32m    moment.init_app(app)[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
[32m+[m[32mdef register_blueprints(app):[m[41m[m
[32m+[m[32m    app.register_blueprint(main_bp)[m[41m[m
[32m+[m[32m    app.register_blueprint(admin_bp, url_prefix='/admin')[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
[32m+[m[32mdef register_template_context(app):[m[41m[m
[32m+[m[32m    @app.context_processor[m[41m[m
[32m+[m[32m    def make_template_context():[m[41m[m
[32m+[m[32m        admin = Admin.query.first()[m[41m[m
[32m+[m[32m        categories = Category.query.order_by(Category.id.asc()).all()[m[41m[m
[32m+[m[32m        subjects = Subject.query.order_by(Subject.id.asc()).all()[m[41m[m
[32m+[m[32m        brands = Brand.query.order_by(Brand.id.asc()).all()[m[41m[m
[32m+[m[32m        all_news_limit = News.query.filter(News.status == True).order_by(News.clicks.desc()).limit(10).all()[m[41m[m
[32m+[m[32m        news_categories = NewsCategory.query.filter(NewsCategory.status == True).order_by(NewsCategory.id.asc()).all()[m[41m[m
[32m+[m[32m        intro_categories = ([m[41m[m
[32m+[m[32m            IntroduceCategory.query[m[41m[m
[32m+[m[32m            .join(IntroduceCategory.introduces)[m[41m[m
[32m+[m[32m            .filter(Introduce.status == True)[m[41m[m
[32m+[m[32m            .options(contains_eager(IntroduceCategory.introduces))[m[41m[m
[32m+[m[32m            .order_by(IntroduceCategory.id.asc())[m[41m[m
[32m+[m[32m            .all()[m[41m[m
[32m+[m[32m        )[m[41m[m
[32m+[m[32m        research_categories = ([m[41m[m
[32m+[m[32m            ResearchCategory.query[m[41m[m
[32m+[m[32m            .join(ResearchCategory.researchs)[m[41m[m
[32m+[m[32m            .filter(Research.status == True)[m[41m[m
[32m+[m[32m            .options(contains_eager(ResearchCategory.researchs))[m[41m[m
[32m+[m[32m            .order_by(ResearchCategory.id.asc())[m[41m[m
[32m+[m[32m            .all()[m[41m[m
[32m+[m[32m        )[m[41m[m
[32m+[m[32m        contact_categories = ([m[41m[m
[32m+[m[32m            ContactCategory.query[m[41m[m
[32m+[m[32m            .join(ContactCategory.contacts)[m[41m[m
[32m+[m[32m            .filter(Contact.status == True)[m[41m[m
[32m+[m[32m            .options(contains_eager(ContactCategory.contacts))[m[41m[m
[32m+[m[32m            .order_by(ContactCategory.id.asc())[m[41m[m
[32m+[m[32m            .all()[m[41m[m
[32m+[m[32m        )[m[41m[m
[32m+[m[32m        hot_products = Product.query.filter(Product.clicks > 0, Product.status == True).order_by([m[41m[m
[32m+[m[32m            Product.clicks.desc()).limit(15)[m[41m[m
[32m+[m[32m        return dict(admin=admin, categories=categories, subjects=subjects, brands=brands,[m[41m[m
[32m+[m[32m                    news_categories=news_categories, contact_categories=contact_categories,[m[41m[m
[32m+[m[32m                    all_news_limit=all_news_limit, hot_products=hot_products,intro_categories=intro_categories,[m[41m[m
[32m+[m[32m                    research_categories=research_categories)[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
[32m+[m[32mdef register_shell_context(app):[m[41m[m
[32m+[m[32m    @app.shell_context_processor[m[41m[m
[32m+[m[32m    def make_shell_context():[m[41m[m
[32m+[m[32m        return dict(db=db)[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
[32m+[m[32mdef register_errorhandlers(app):[m[41m[m
[32m+[m[32m    @app.errorhandler(400)[m[41m[m
[32m+[m[32m    def bad_request(e):[m[41m[m
[32m+[m[32m        return render_template('errors/400.html'), 400[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    @app.errorhandler(403)[m[41m[m
[32m+[m[32m    def forbidden(e):[m[41m[m
[32m+[m[32m        return render_template('errors/403.html'), 403[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    @app.errorhandler(404)[m[41m[m
[32m+[m[32m    def page_not_found(e):[m[41m[m
[32m+[m[32m        return render_template('errors/404.html'), 404[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    @app.errorhandler(413)[m[41m[m
[32m+[m[32m    def request_entity_too_large(e):[m[41m[m
[32m+[m[32m        return render_template('errors/413.html'), 413[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    @app.errorhandler(500)[m[41m[m
[32m+[m[32m    def internal_server_error(e):[m[41m[m
[32m+[m[32m        return render_template('errors/500.html'), 500[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    @app.errorhandler(CSRFError)[m[41m[m
[32m+[m[32m    def handle_csrf_error(e):[m[41m[m
[32m+[m[32m        return render_template('errors/400.html', description=e.description), 400[m[41m[m
[32m+[m[41m[m
[32m+[m[41m[m
[32m+[m[32mdef register_commands(app):[m[41m[m
[32m+[m[32m    @app.cli.command()[m[41m[m
[32m+[m[32m    @click.option('--drop', is_flag=True, help='Create after drop.')[m[41m[m
[32m+[m[32m    def initdb(drop):[m[41m[m
[32m+[m[32m        if drop:[m[41m[m
[32m+[m[32m            click.confirm('This operation will delete the database, do you want to continue?', abort=True)[m[41m[m
[32m+[m[32m            db.drop_all()[m[41m[m
[32m+[m[32m            click.echo('Drop tables...')[m[41m[m
[32m+[m[32m        db.create_all()[m[41m[m
[32m+[m[32m        click.echo('Initialized database...')[m[41m[m
[32m+[m[32m        Category.get_default_category()[m[41m[m
[32m+[m[32m        Brand.get_default_brand()[m[41m[m
[32m+[m[32m        Subject.get_default_subject()[m[41m[m
[32m+[m[32m        click.echo('Initialized default category, Brand, Subject...')[m[41m[m
[32m+[m[41m[m
[32m+[m[32m    @app.cli.command()[m[41m[m
[32m+[m[32m    @click.option('--product', default=30, help='Quantity of products, default is 30.')[m[41m[m
[32m+[m[32m    @click.option('--news', default=30, help='Quantity of products, default is 30.')[m[41m[m
[32m+[m[32m    @click.option('--introduce', default=5, help='Quantity of introduce, default is 5.')[m[41m[m
[32m+[m[32m    @click.option('--research', default=3, help='Quantity of research and development, default is 3.')[m[41m[m
[32m+[m[32m    @click.option('--contact', default=3, help='Quantity of contact, default is 3.')[m[41m[m
[32m+[m[32m    @click.option('--photo', default=50, help='Quantity of photos, default is 50.')[m[41m[m
[32m+[m[32m    def forge(product, news, introduce, contact, photo, research):[m[41m[m
[32m+[m[32m        from .fakes import fake_categories, admin, fake_products, news_categories, fake_news, intro_category, \[m[41m[m
[32m+[m[32m            fake_intro, fake_brand, fake_subject, contact_categories, fake_contact, fake_photo, research_category, \[m[41m[m
[32m+[m[32m            fake_research, fake_index_about, fake_banners[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Drop tables....')[m[41m[m
[32m+[m[32m        db.drop_all()[m[41m[m
[32m+[m[32m        click.echo('Initialized database......')[m[41m[m
[32m+[m[32m        db.create_all()[m[41m[m
[32m+[m[32m        Category.get_default_category()[m[41m[m
[32m+[m[32m        Brand.get_default_brand()[m[41m[m
[32m+[m[32m        Subject.get_default_subject()[m[41m[m
[32m+[m[32m        click.echo('Generating default category, Brand, Subject...')[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating the administrator...')[m[41m[m
[32m+[m[32m        admin()[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating product_categories...')[m[41m[m
[32m+[m[32m        fake_categories()[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating brand and subject...')[m[41m[m
[32m+[m[32m        fake_brand()[m[41m[m
[32m+[m[32m        fake_subject()[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating %d products...' % product)[m[41m[m
[32m+[m[32m        fake_products(product)[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating %d photos...' % photo)[m[41m[m
[32m+[m[32m        fake_photo(photo)[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating news_categories and %d news...' % news)[m[41m[m
[32m+[m[32m        news_categories()[m[41m[m
[32m+[m[32m        fake_news(news)[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating research_categories and %d research contents...' % research)[m[41m[m
[32m+[m[32m        research_category()[m[41m[m
[32m+[m[32m        fake_research(research)[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating contact_category and %d contact' % contact)[m[41m[m
[32m+[m[32m        contact_categories()[m[41m[m
[32m+[m[32m        fake_contact(contact)[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating intro_categories and %d introduce...' % introduce)[m[41m[m
[32m+[m[32m        intro_category()[m[41m[m
[32m+[m[32m        fake_intro(introduce)[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating index_about...')[m[41m[m
[32m+[m[32m        fake_index_about()[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Generating banner photos...')[m[41m[m
[32m+[m[32m        fake_banners()[m[41m[m
[32m+[m[41m[m
[32m+[m[32m        click.echo('Done!')[m[41m[m
