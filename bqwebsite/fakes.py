import os
import random

import click
from PIL import Image
from faker import Faker
from faker.providers import DynamicProvider
from flask import current_app

from .models import Admin, Category, Product, NewsCategory, News, IntroduceCategory, Introduce, Subject, Brand, \
    Contact, ContactCategory, Photo, ResearchCategory, Research
from .extensions import db
from .utils import generate_gradient_image

fake = Faker('zh_CN')

fake_products = DynamicProvider(
    provider_name='products',
    elements=[
        '桂龙药膏',
        '止咳平喘膏',
        '麻杏止咳膏',
        '咳喘停膏',
        '感冒灵冲剂(块状)',
        '三参益气口服液',
        '小儿化痰止咳糖浆',
        '抗宫炎颗粒',
        '百咳静糖浆',
        '感冒灵颗粒',
        '川贝止咳露',
        '健儿消食口服液',
        '安乐片',
        '安胎益母丸',
        '八珍益母膏',
        '百梅止咳颗粒',
        '半夏糖浆',
        '参芪首乌补汁',
        '陈香露白露片',
        '跌打扭伤灵酊',
        '复方丹参片',
        '桂龙药酒',
        '复方鱼腥草颗粒',
        '复方双花藤止痒搽剂',
        '藿香正气合剂',
        '穿金益肝片',
        '复方愈创木酚磺酸钾口服溶液',
        '清感穿心莲片',
        '止咳枇杷颗粒',
        '桂圆琼玉冲剂',
        '伤痛酊',
        '复方羊角颗粒',
        '三维葡磷钙咀嚼片',
        '橘红痰咳颗粒'

    ],  # 34 products
)

fake.add_provider(fake_products)


def admin():
    admin = Admin(
        email='46361381@qq.com',
        name='Admin',
    )
    admin.set_password('123456')
    db.session.add(admin)
    db.session.commit()


def fake_categories():
    jixing = ['膏剂', '散剂', '片剂', '胶囊', '搽剂', '颗粒剂', '糖浆', '酊剂', '其他']

    for i in jixing:
        category = Category(name=i)
        db.session.add(category)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()


def fake_subject():
    sub = ['补益类', '儿童用药', '妇科用药', '感冒咳嗽', '护理保健', '其他功能']

    for i in sub:
        subject = Subject(name=i)
        db.session.add(subject)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()


def fake_brand():
    bra = ['邦琪', '葛洪', '原方', '金鸡', '汉森元', '康司臣', '多通葆', '比愈通', '其他']

    for i in bra:
        brand = Brand(name=i)
        db.session.add(brand)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()


def fake_products(count=30):
    unique_product = set()
    for i in range(count):
        while True:
            product_name = fake.products()
            if product_name not in unique_product:
                unique_product.add(product_name)
                click.echo('Generated unique product name: %s' % product_name)
                break

        product = Product(
            name=product_name,
            product_indication=fake.text(50),
            product_content=fake.text(300),
            product_format=fake.text(5),
            category=Category.query.get(random.randint(1, Category.query.count())),
            brand=Brand.query.get(random.randint(1, Brand.query.count())),
            subject=Subject.query.get(random.randint(1, Subject.query.count())),
            clicks=random.randint(1, 5000),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(product)
    db.session.commit()


def fake_photo(count=50):
    for i in range(count):
        filename = 'random_%d.jpg' % i
        generate_gradient_image(600, 700, filename)

        photo = Photo(
            filename_s=filename,
            filename_m=filename,
            filename=filename,
            product=Product.query.get(random.randint(1, Product.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(photo)
    db.session.commit()


def news_categories():
    news_cate = ['公司新闻', '行业资讯', '家庭护理', '商标展示']

    for i in news_cate:
        category = NewsCategory(
            name=i,
            timestamp=fake.date_time_this_year()
        )

        db.session.add(category)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()


def fake_news(count=80):
    for i in range(count):
        news = News(
            title=fake.sentence(),
            content=fake.text(200),
            newscategory=NewsCategory.query.get(random.randint(1, NewsCategory.query.count())),
            timestamp=fake.date_time_this_year(),
            clicks=fake.random.randint(10, 500)
        )
        db.session.add(news)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()


def intro_category():
    intro_cate = ['集团介绍', '质量机构', '企业架构', '社会责任', '企业荣誉']

    for i in intro_cate:
        category = IntroduceCategory(
            name=i,
            timestamp=fake.date_time_this_year()
        )

        db.session.add(category)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()


def fake_intro(count=5):
    for i in range(count):
        intro = Introduce(
            title=fake.sentence(),
            introduce_content=fake.text(200),
            timestamp=fake.date_time_this_year(),
            introduce_category=IntroduceCategory.query.get(i + 1)
        )
        db.session.add(intro)
    db.session.commit()

def research_category():
    res_cat = ['产品研发', '质量机构', '生产车间']

    for i in res_cat:
        category = ResearchCategory(name=i, timestamp=fake.date_time_this_year())
        db.session.add(category)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()

def fake_research(count=3):
    for i in range(count):
        research = Research(
            title=fake.sentence(),
            research_content=fake.text(200),
            timestamp=fake.date_time_this_year(),
            research_category=ResearchCategory.query.get(i + 1)
        )
        db.session.add(research)
    db.session.commit()

def contact_categories():
    cont_cat = ['联系方式', '商业合作', '企业招聘']

    for i in cont_cat:
        category = ContactCategory(name=i)
        db.session.add(category)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()


def fake_contact(count=3):
    for i in range(count):
        contact = Contact(
            title=fake.sentence(),
            content=fake.text(200),
            timestamp=fake.date_time_this_year(),
            contact_category=ContactCategory.query.get(i + 1)
        )
        db.session.add(contact)
    db.session.commit()
