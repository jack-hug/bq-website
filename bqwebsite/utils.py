import os
import time
import uuid
from urllib.parse import urlparse, urljoin

from .models import Photo

from PIL import Image, ImageDraw
import random
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

def resize_image(image_path, filename, base_width, base_height):
    filename, ext = os.path.splitext(filename)
    img = Image.open(image_path)

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

def save_temp_files(file):
    if not os.path.exists(current_app.config['BQ_TEMP_FOLDER']):
        os.makedirs(current_app.config['BQ_TEMP_FOLDER'])
    filename = random_filename(file.filename)
    file_path = os.path.join(current_app.config['BQ_TEMP_FOLDER'], filename)
    file.save(file_path)
    return filename

def save_upload_files(file):
    if not os.path.exists(current_app.config['BQ_UPLOAD_PATH']):
        os.makedirs(current_app.config['BQ_UPLOAD_PATH'])
    filename = random_filename(file.filename)
    file_path = os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename)
    file.save(file_path)
    return filename
def save_uploaded_files(request_files, product_id):  # 封装上传图片函数
    photos = []
    for f in request_files.getlist('file'):
        if f.content_length > current_app.config['MAX_CONTENT_LENGTH']:
            flash(f'文件 {f.filename} 过大，上传的文件大小不能超过5MB')
            continue
        filename = random_filename(f.filename)
        f.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
        filename_s = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['small'],
                                  current_app.config['BQ_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['BQ_PHOTO_SIZE']['medium'],
                                  current_app.config['BQ_PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            product_id=product_id
        )
        photos.append(photo)
    return photos

def generate_gradient_image(width, height, filename):  # 生成随机渐变图片
    img = Image.new(mode='RGB', size=(width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Define the gradient colors
    start_color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
    end_color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))

    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y / height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y / height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    upload_path = current_app.config['BQ_UPLOAD_PATH']
    img.save(os.path.join(upload_path, filename))

def clean_temp_folder():  # 定时清除临时文件夹的文件
    now = time.time()
    for filename in os.listdir(current_app.config['BQ_TEMP_FOLDER']):
        file_path = os.path.join(current_app.config['BQ_TEMP_FOLDER'], filename)
        if os.path.getmtime(file_path) < now - 3600:
            os.remove(file_path)
