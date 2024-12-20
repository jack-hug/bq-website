from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, MultipleFileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from ..models import Category, Brand, Subject, Product
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登 录')


class ProductForm(FlaskForm):
    name = StringField('产品名称:', validators=[DataRequired(), Length(1, 128)],
                       render_kw={'placeholder': '请输入产品名称'})
    category = SelectField('产品分类:', coerce=int, default=1)
    brand = SelectField('商标:', coerce=int, default=1)
    subject = SelectField('功能分类:', coerce=int, default=1)
    product_indication = StringField('功能主治:', validators=[DataRequired(), Length(1, 1024)])
    product_format = StringField('产品规格:', validators=[])
    product_content = CKEditorField('产品内容:', validators=[DataRequired()])
    photos = MultipleFileField('产品图片:', validators=[])
    submit = SubmitField('确认添加')
    cancel = SubmitField('取 消')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
        self.brand.choices = [(brand.id, brand.name) for brand in Brand.query.all()]
        self.subject.choices = [(subject.id, subject.name) for subject in Subject.query.all()]

    def validate_name(self, field):
        if Product.query.filter_by(name=field.data).first():
            raise ValidationError('该产品已存在，可以在产品后添加规格以作区分')


class EditProductForm(FlaskForm):
    name = StringField('产品名称:', validators=[DataRequired(), Length(1, 128)])
    category = SelectField('产品分类:', coerce=int, default=1)
    brand = SelectField('商标:', coerce=int, default=1)
    subject = SelectField('功能分类:', coerce=int, default=1)
    product_indication = StringField('功能主治:', validators=[DataRequired(), Length(1, 1024)])
    product_format = StringField('产品规格:', validators=[DataRequired()])
    product_content = CKEditorField('产品内容:', validators=[DataRequired()])
    photos = MultipleFileField('产品图片:', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只能上传图片')])
    submit = SubmitField('确认修改')
    cancel = SubmitField('取消')

    def __init__(self, *args, **kwargs):  # 产品类别
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]
        self.brand.choices = [(brand.id, brand.name) for brand in Brand.query.all()]
        self.subject.choices = [(subject.id, subject.name) for subject in Subject.query.all()]


class CategoryForm(FlaskForm):
    name = StringField('剂型名称', validators=[DataRequired(), Length(1, 128)])
    category_submit = SubmitField('提交', name='category_submit')

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('该剂型已存在')


class BrandForm(FlaskForm):
    name = StringField('商标名称', validators=[DataRequired(), Length(1, 128)])
    brand_submit = SubmitField('提交', name='brand_submit')

    def validate_name(self, field):
        if Brand.query.filter_by(name=field.data).first():
            raise ValidationError('该商标已存在')


class SubjectForm(FlaskForm):
    name = StringField('功能主治名称', validators=[DataRequired(), Length(1, 128)])
    subject_submit = SubmitField('提交', name='subject_submit')

    def validate_name(self, field):
        if Subject.query.filter_by(name=field.data).first():
            raise ValidationError('该类型已存在')


class EditCategoryForm(FlaskForm):
    name = StringField('剂型名称', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('修改')

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('该剂型已存在')


class EditBrandForm(FlaskForm):
    name = StringField('商标名称', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('修改')

    def validate_name(self, field):
        if Brand.query.filter_by(name=field.data).first():
            raise ValidationError('该商标已存在')


class EditSubjectForm(FlaskForm):
    name = StringField('功能名称', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('修改')

    def validate_name(self, field):
        if Subject.query.filter_by(name=field.data).first():
            raise ValidationError('该功能分类已存在')
