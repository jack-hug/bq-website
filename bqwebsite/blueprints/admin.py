from flask import render_template, Blueprint

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def index():
    return render_template('admin/index.html')


@admin_bp.route('/profile')
def profile():
    return render_template('admin/pages/profile.html')


@admin_bp.route('/change-password')
def password():
    return render_template('admin/pages/password.html')


@admin_bp.route('/welcome')
def welcome():
    return render_template('admin/pages/welcome.html')


@admin_bp.route('/user_list')
def user_list():
    return render_template('admin/pages/user.html')


@admin_bp.route('/role')
def role():
    return render_template('admin/pages/role.html')


@admin_bp.route('/node')
def node():
    return render_template('admin/pages/node.html')


@admin_bp.route('/blank')
def blank():
    return render_template('admin/pages/blank.html')


@admin_bp.route('/lockscreen')
def lockscreen():
    return render_template('admin/pages/lockscreen.html')


@admin_bp.route('/gallery')
def gallery():
    return render_template('admin/pages/gallery.html')


@admin_bp.route('/errors')
def errors():
    return render_template('admin/pages/errors.html')


@admin_bp.route('/login')
def login():
    return render_template('admin/pages/login.html')


@admin_bp.route('/timeline')
def timeline():
    return render_template('admin/pages/timeline.html')


@admin_bp.route('/layout1')
def layout1():
    return render_template('admin/pages/layout1.html')


@admin_bp.route('/layout2')
def layout2():
    return render_template('admin/pages/layout2.html')


@admin_bp.route('/layout3')
def layout3():
    return render_template('admin/pages/layout3.html')

@admin_bp.route('/plugin-day-js')
def plugin_day_js():
    return render_template('admin/pages/plugin-day.js.html')

@admin_bp.route('/plugin-clipboard')
def plugin_clipboard():
    return render_template('admin/pages/plugin-clipboard.html')

@admin_bp.route('/plugin-shepherd')
def plugin_shepherd():
    return render_template('admin/pages/plugin-shepherd.html')

@admin_bp.route('/plugin-fullcalendar')
def plugin_fullcalendar():
    return render_template('admin/pages/plugin-fullcalendar.html')

@admin_bp.route('/plugin-video-js')
def plugin_video_js():
    return render_template('admin/pages/plugin-video-js.html')

@admin_bp.route('/plugin-pickr')
def plugin_pickr():
    return render_template('admin/pages/plugin-pickr.html')

@admin_bp.route('/plugin-raty-js')
def plugin_raty_js():
    return render_template('admin/pages/plugin-raty-js.html')

@admin_bp.route('/plugin-bootstrap-input-spinner')
def plugin_bootstrap_input_spinner():
    return render_template('admin/pages/plugin-bootstrap-input-spinner.html')

@admin_bp.route('/plugin-bs-stepper')
def plugin_bs_stepper():
    return render_template('admin/pages/plugin-bs-stepper.html')

@admin_bp.route('/plugin-sweetalert2')
def plugin_sweetalert2():
    return render_template('admin/pages/plugin-sweetalert2.html')

@admin_bp.route('/plugin-formvalidation')
def plugin_formvalidation():
    return render_template('admin/pages/plugin-formvalidation.html')

@admin_bp.route('/plugin-tempus-dominus')
def plugin_tempus_dominus():
    return render_template('admin/pages/plugin-tempus-dominus.html')

@admin_bp.route('/plugin-croppie')
def plugin_croppie():
    return render_template('admin/pages/plugin-croppie.html')

@admin_bp.route('/plugin-ztree')
def plugin_ztree():
    return render_template('admin/pages/plugin-ztree.html')

@admin_bp.route('/plugin-chart')
def plugin_chart():
    return render_template('admin/pages/plugin-chart.html')

@admin_bp.route('/plugin-echarts')
def plugin_echarts():
    return render_template('admin/pages/plugin-echarts.html')

@admin_bp.route('/plugin-bootstrap-table')
def plugin_bootstrap_table():
    return render_template('admin/pages/plugin-bootstrap-table.html')

@admin_bp.route('/plugin-datatables')
def plugin_datatables():
    return render_template('admin/pages/plugin-datatables.html')

@admin_bp.route('/plugin-wangeditor')
def plugin_wangeditor():
    return render_template('admin/pages/plugin-wangeditor.html')

@admin_bp.route('/plugin-bootstrap-fileinput')
def plugin_bootstrap_fileinput():
    return render_template('admin/pages/plugin-bootstrap-fileinput.html')

@admin_bp.route('/plugin-dropzone')
def plugin_dropzone():
    return render_template('admin/pages/plugin-dropzone.html')

@admin_bp.route('/plugin-select2')
def plugin_select2():
    return render_template('admin/pages/plugin-select2.html')

@admin_bp.route('/plugin-bootstrap-select')
def plugin_bootstrap_select():
    return render_template('admin/pages/plugin-bootstrap-select.html')

@admin_bp.route('/plugin-fonticonpicker')
def plugin_fonticonpicker():
    return render_template('admin/pages/plugin-fonticonpicker.html')

@admin_bp.route('/sys-email')
def sys_email():
    return render_template('admin/pages/sys_email.html')

@admin_bp.route('/sys-website')
def sys_website():
    return render_template('admin/pages/sys_website.html')

@admin_bp.route('/search')
def search():
    return render_template('admin/pages/search.html')

@admin_bp.route('/message')
def message():
    return render_template('admin/pages/message.html')
