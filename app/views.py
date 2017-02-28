from flask import render_template, request, url_for, jsonify, redirect
from flask_login import login_required, login_user, logout_user, LoginManager, UserMixin, \
    current_user
from app.activedirectory import UserAuthentication
from functools import wraps
from producers.StarLims import StarLimsApi
from producers.eqaAPI import EqaAPI
from queries import get_user_by_username
from mod_admin.queries import check_if_admin
from app.performance_summary import s, app
from forms import *

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, password=None):
        self.id = id
        self.password = password

    def is_authenticated(self, s, id, password):
        validuser = get_user_by_username(s, id)
        if len(list(validuser)) == 0:
            return False
        else:
            check_activdir = UserAuthentication().authenticate(id, password)

            if check_activdir != "False":
                return True
            else:
                return False

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if check_if_admin(s,current_user.id) is False:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('home.html', panels=3)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login(next=request.args.get('next'))
    if request.method == 'GET':
        return render_template("login.html", form=form)
    elif request.method == 'POST':
        user = User(form.data["username"], password=form.data["password"])
        result = user.is_authenticated(s, id=form.data["username"], password=form.data["password"])
        if result:
            login_user(user)

            if form.data["next"] != "":
                return redirect(form.data["next"])
            else:
                return redirect(url_for('index'))
        else:
            return render_template("login.html", form=form, modifier="Oh Snap!", message="Wrong username or password")




@app.route("/logout")
@login_required
def logout():
    # todo unlock all users locked
    app.logger.info("logout")
    logout_user()
    form = Login()
    return render_template("login.html", form=form, message="You have logged out!")

@app.context_processor
def logged_in():
    if current_user.is_authenticated:
        userid = current_user.id
        admin=check_if_admin(s,userid)

        #app.logger.basicConfig(format='%(levelname)s|'+ current_user.id+'|%(asctime)s|%(message)s')
        return {'logged_in': True, 'userid': userid,'admin':admin}
    else:
        return {'logged_in': False}