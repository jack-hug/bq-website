import random

from faker import Faker

from bqwebsite.models import Admin, Category, Product, NewsCategory, News, IntroduceCategory, Introduce, Subject, Brand, \
    Contact, ContactCategory
from bqwebsite.extensions import db

fake = Faker('zh_CN')


def admin():
    admin = Admin(
        email='46361381@qq.com',
        name='Admin',
    )
    admin.set_password('123456')
    db.session.add(admin)
    db.session.commit()


def categories():
    category = Category(product_category='Default')
    db.session.add(category)

    jixing = ['膏剂', '散剂', '片剂', '胶囊', '搽剂', '颗粒剂', '糖浆', '酊剂']

    for i in jixing:
        category = Category(product_category=i)
        db.session.add(category)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()

def subject():
    subject = Subject(name='Default')
    db.session.add(subject)

    sub = ['补益类', '儿童用药', '妇科用药', '感冒咳嗽', '护理保健']

    for i in sub:
        subject = Subject(name=i)
        db.session.add(subject)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()

def brand():
    brand = Brand(name='Default')
    db.session.add(brand)

    bra = ['葛洪', '邦琪', '原方', '金鸡', '汉森元', '康司臣', '其他']

    for i in bra:
        brand = Brand(name=i)
        db.session.add(brand)
    try:
        db.session.commit()
    except InterruptedError:
        db.session.rollback()

def fake_products(count=50):
    for i in range(count):
        product = Product(
            product_name=fake.sentence(3),
            product_indication=fake.text(50),
            product_manual=fake.text(50),
            product_content=fake.text(50),
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )
        db.session.add(product)
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
    intro_cate = ['公司介绍', '质量机构', '企业架构', '社会责任', '企业荣誉']

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
            introduce_category=IntroduceCategory.query.get(i+1)
        )
        db.session.add(intro)
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
            contact_category=ContactCategory.query.get(i+1)
        )
        db.session.add(contact)
    db.session.commit()



