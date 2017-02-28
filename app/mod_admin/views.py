from collections import OrderedDict

from app.queries import get_users, get_username_by_user_id
from queries import check_if_admin, get_user_id_by_username
from flask import Blueprint
from flask import render_template, request, url_for, redirect
from flask.ext.login import login_required, current_user

from app.performance_summary import s
from app.views import admin_required
from flask_table import Table, Col, LinkCol
from forms import UserForm
from queries import create_user, toggle_admin_query


class ItemTableUsers(Table):
    username = Col('User')
    admin = Col('Admin')
    toggle_admin = LinkCol('Toggle Admin', 'admin.toggle_admin', url_kwargs=dict(id='id'))


class ItemTableLocked(Table):
    name = Col('Panel')
    username = Col('Locked By')
    toggle_lock = LinkCol('Toggle Lock', 'admin.toggle_locked', url_kwargs=dict(id='id'))


admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/user', methods=['GET', 'POST'])
@login_required
@admin_required
def user_admin():
    """
    view to allow users to be added and admin rights toggled

    :return: render html template
    """
    form = UserForm()
    message = None
    if request.method == 'POST':
        username = request.form["name"]
        if check_if_admin(s, current_user.id):
            create_user(s, username)
            message = "Added user: " + username
        else:
            return render_template('users.html', form=form, message="You can't do that")
    users = get_users(s)
    result = []
    for i in users:
        if i.username != current_user.id:
            row = dict(zip(i.keys(), i))
            result.append(row)
    table = ItemTableUsers(result, classes=['table', 'table-striped'])
    return render_template('users.html', form=form, table=table, message=message)


@admin.route('/user/toggle', methods=['GET', 'POST'])
@login_required
@admin_required
def toggle_admin():
    """
    toggles admin rights of a user

    :return: redirect to user_admin
    """
    user_id = request.args.get('id')
    toggle_admin_query(s, user_id)
    return redirect(url_for('admin.user_admin'))



@admin.route('/logs', methods=['GET', 'POST'])
@login_required
@admin_required
def view_logs():
    """
    view admin logs so that you can see what users have been doing

    :return: render hmtl template
    """
    if request.args.get('file'):
        log = request.args.get('file')
    else:
        log = 'PanelPal.log'

    import glob
    files = []
    listing = glob.glob('*log*')
    for filename in listing:
        files.append(filename)

    result = []
    with open(log) as f:
        for line in f:
            result.append(line.rstrip())

    return render_template('logs.html', log=result, files=files)

