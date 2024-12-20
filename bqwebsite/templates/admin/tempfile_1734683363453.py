# D:\git\bq-website\bqwebsite\blueprints\admin.py
@admin_bp.route('/product/new', methods=['GET', 'POST'])  # 新建产品
@login_required
def product_add():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            product_content=form.product_content.data,
            product_indication=form.product_indication.data,
            product_format=form.product_format.data,
            category_id=form.category.data,
            brand_id=form.brand.data,
            subject_id=form.subject.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(product)
        db.session.commit()

        if 'photos' in request.files:
            photos = []
            for file in request.files.getlist('photos'):
                if file and allowed_file(file.filename):
                    filename = random_filename(file.filename)
                    file_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename)
                    file.save(file_path)
                    photo = Photo(filename=filename, product=product)
                    photos.append(photo)
            db.session.add_all(photos)
            db.session.commit()
        
        flash('添加成功.', 'success')
        return redirect(url_for('admin.product_list'))
    
    return render_template('admin/product_add.html', form=form, show_collapse=True)
