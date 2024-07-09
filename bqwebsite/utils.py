import os
import uuid
from urllib.parse import urlparse, urljoin

import PIL
from PIL import Image
from flask import request, redirect, url_for, current_app


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

def resize_image(image, filename, base_width):
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    if img.size[0] <= base_width:
        return filename + ext
    w_percent = (base_width / float(img.size[0]))
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), PIL.Image.Resampling.LANCZOS)

    filename += current_app.config['BQ_PHOTO_SUFFIX'][base_width] + ext
    img.save(os.path.join(current_app.config['BQ_UPLOAD_PATH'], filename))
    return filename
