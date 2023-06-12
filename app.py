from flask import Flask, render_template
from models import Categories, Products, News, Brand, Honor, Banner, Introduce
from exts import db
from flask_migrate import Migrate
import config
app = Flask(__name__)

intro = {
    'introduce': '广西邦琪药业集团有限公司是一家已有20'
                 '多年的发展历史的民营制药企业，连续入榜广西民营制造业百强、广西高新技术企业百强行列，是广西优秀企业，是集科研、生产、销售、服务为一体的综合性企业集团。集团公司旗下现有10'
                 '多家子公司，包括百琪药业、葛洪堂药业、邦琪医药、泰和制药等多家医药企业。集团公司在药品的生产销售和药品研发方面有较强的特色和优势，产品资源相当丰富，药品生产批文号350多个，独家品种35个（其中10'
                 '个有新药证书）。主要产品有桂龙药膏、复方鱼腥草颗粒、金鸡胶囊、五参安神口服液、罗汉果止咳膏、黄荆油胶丸、抗宫炎颗粒、三参益气口服液、参芪首乌补汁、咳喘停膏等品种。'
}

app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html', intro=intro)


@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/news_company')
def news_company():
    return render_template('news_company.html')


@app.route('/news_industry')
def news_industry():
    return render_template('news_industry.html')


@app.route('/news_file')
def news_file():
    return render_template('news_file.html')


@app.route('/news_detail')
def news_detail():
    return render_template('news_detail.html')


@app.route('/product')
def product():
    return render_template('product.html')

@app.route('/product_categories')
def proudct_categories():
    return render_template('product_categories.html')

@app.route('/product_detail')
def product_detail():
    return render_template('product_detail.html')


@app.route('/introduce')
def introduce():
    return render_template('introduce.html')


@app.route('/honor')
def honor():
    return render_template('honor.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run()
