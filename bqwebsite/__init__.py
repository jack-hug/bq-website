import click
import os

from flask import Flask, render_template

from bqwebsite.blueprints.main import main_bp
from bqwebsite.blueprints.admin import admin_bp
from bqwebsite.config import config
from bqwebsite.extensions import bootstrap, db, csrf, dropzone, login_manager
from bqwebsite.models import Category, Product, News, Brand, Honor, Banner, Introduce, Photo, NewsCategory, \
    IntroduceCategory, Admin, Subject, ContactCategory


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bqwebsite')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_errorhandlers(app)
    register_commands(app)
    register_template_context(app)

    return app


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    csrf.init_app(app)
    dropzone.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.id.asc()).all()
        subjects = Subject.query.order_by(Subject.id.asc()).all()
        brands = Brand.query.order_by(Brand.id.asc()).all()
        all_news_limit = News.query.order_by(News.clicks.desc()).limit(10).all()
        news_categories = NewsCategory.query.order_by(NewsCategory.id.asc()).all()
        introduce_categories = IntroduceCategory.query.order_by(IntroduceCategory.id.asc()).all()
        contact_categories = ContactCategory.query.order_by(ContactCategory.id.asc()).all()
        hot_products = Product.query.filter(Product.clicks > 0).order_by(Product.clicks.desc()).limit(15)
        return dict(admin=admin, categories=categories, subjects=subjects, brands=brands,
                    news_categories=news_categories, introduce_categories=introduce_categories,
                    contact_categories=contact_categories, all_news_limit=all_news_limit, hot_products=hot_products)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables...')
        db.create_all()
        click.echo('Initialized database...')

    @app.cli.command()
    @click.option('--product', default=50, help='Quantity of products, default is 50.')
    @click.option('--news', default=80, help='Quantity of products, default is 50.')
    @click.option('--introduce', default=5, help='Quantity of introduce, default is 5.')
    @click.option('--contact', default=3, help='Quantity of contact, default is 3.')
    def forge(product, news, introduce, contact):
        from bqwebsite.fakes import fake_categories, admin, fake_products, news_categories, fake_news, intro_category, \
            fake_intro, fake_brand, fake_subject, contact_categories, fake_contact

        click.echo('Drop tables....')
        db.drop_all()
        click.echo('Initialized database......')
        db.create_all()

        click.echo('Generating the administrator...')
        admin()

        click.echo('Generating product_categories...')
        fake_categories()

        click.echo('Generating brand and subject...')
        fake_brand()
        fake_subject()

        click.echo('Generating %d products...' % product)
        fake_products(product)

        click.echo('Generating news_categories and %d news...' % news)
        news_categories()
        fake_news(news)

        click.echo('Generating contact_category and %d contact' % contact)
        contact_categories()
        fake_contact(contact)

        click.echo('Generating intro_categories and %d introduce...' % introduce)
        intro_category()
        fake_intro(introduce)

        click.echo('Done!')
