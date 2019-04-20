from flask import abort, render_template
from flask_login import current_user, login_required

from . import home
from ..libvirt_test import libvirt_test

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title='Dashboard')

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    run=libvirt_test()
    result,vm_list=run.api_list_domains()
    return render_template('home/dashboard.html', title="Dashboard",vm_list=vm_list)