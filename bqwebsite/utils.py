import os
import uuid
from urllib.parse import urlparse, urljoin
from bqwebsite.models import Photo

import PIL
from PIL import Image
from flask import request, redirect, url_for, current_app, flash


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
        return redirect(url_for(default, **kwargs))


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


# def resize_image(image, filename, base_width):
#     # filename, ext = os.path.splitext(filename)
#     # img = Image.open(image)
#     # if img.size[0] <= base_width:
#     #     return filename + ext
#     # w_percent = (base_width / float(img.size[0]))
#     # h_size = int(float(img.size[1]) * float(w_percent))
#     # img = img.resize((base_width, h_size), PIL.Image.Resampling.LANCZOS)
#     #
#     # filename += current_app.config['BQ_PHOTO_SUFFIX'][base_width] + ext
#     # img.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
#     # return filename
def resize_image(image, filename, base_width, base_height):
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)

    # Determine the maximum dimension
    max_dimension = max(img.size[0], img.size[1])

    if max_dimension <= max(base_width, base_height):
        return filename + ext

    # Calculate the new dimensions
    if img.size[0] > img.size[1]:
        w_percent = (base_width / float(img.size[0]))
        h_size = int(float(img.size[1]) * float(w_percent))
        new_size = (base_width, h_size)
    else:
        h_percent = (base_height / float(img.size[1]))
        w_size = int(float(img.size[0]) * float(h_percent))
        new_size = (w_size, base_height)

    img = img.resize(new_size, Image.Resampling.LANCZOS)

    filename += current_app.config['BQ_PHOTO_SUFFIX'][max(base_width, base_height)] + ext
    img.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
    return filename


def save_uploaded_files(request_files, product):  # 封装上传图片函数
    photos = []
    for f in request_files.getlist('photos'):
        if f.content_length > current_app.config['MAX_CONTENT_LENGTH']:
            flash(f'文件 {f.filename} 过大，上传的文件大小不能超过3MB')
            continue
        filename = random_filename(f.filename)
        f.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
        # filename_s = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['small'])
        # filename_m = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['medium'])
        filename_s = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['small'], current_app.config['BQ_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['medium'], current_app.config['BQ_PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            product=product
        )
        photos.append(photo)
    return photos
