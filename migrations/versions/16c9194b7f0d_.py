"""empty message

Revision ID: 16c9194b7f0d
Revises: 
Create Date: 2023-06-21 10:25:26.587102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16c9194b7f0d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('banner', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_banner_timestamp'), ['timestamp'], unique=False)

    op.create_table('brand',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('brand_name', sa.String(length=100), nullable=True),
    sa.Column('brand_category', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_category', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_categories_timestamp'), ['timestamp'], unique=False)

    op.create_table('honor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('honor_title', sa.String(length=100), nullable=True),
    sa.Column('honor_img', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('introducecategory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('introduce_category', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('newscategory',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('news_categories', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('newscategory', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_newscategory_timestamp'), ['timestamp'], unique=False)

    op.create_table('introduce',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('list', sa.String(length=100), nullable=True),
    sa.Column('introduce_content', sa.Text(), nullable=True),
    sa.Column('introduce_category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['introduce_category_id'], ['introducecategory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('news',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('news_title', sa.String(length=100), nullable=True),
    sa.Column('news_content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('newscategory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['newscategory_id'], ['newscategory.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_news_timestamp'), ['timestamp'], unique=False)

    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('product_name', sa.String(length=100), nullable=True),
    sa.Column('product_indication', sa.String(length=200), nullable=True),
    sa.Column('product_manual', sa.Text(), nullable=True),
    sa.Column('product_content', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('clicks', sa.Integer(), nullable=True),
    sa.Column('categories_id', sa.Integer(), nullable=True),
    sa.Column('brand_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['categories_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_products_timestamp'), ['timestamp'], unique=False)

    op.create_table('productimage',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('filename', sa.String(length=100), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('products_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['products_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('productimage', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_productimage_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('productimage', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_productimage_timestamp'))

    op.drop_table('productimage')
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_products_timestamp'))

    op.drop_table('products')
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_news_timestamp'))

    op.drop_table('news')
    op.drop_table('introduce')
    with op.batch_alter_table('newscategory', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_newscategory_timestamp'))

    op.drop_table('newscategory')
    op.drop_table('introducecategory')
    op.drop_table('honor')
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_categories_timestamp'))

    op.drop_table('categories')
    op.drop_table('brand')
    with op.batch_alter_table('banner', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_banner_timestamp'))

    op.drop_table('banner')
    # ### end Alembic commands ###