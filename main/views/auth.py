from flask import Blueprint, render_template, request, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import functools

from main import db
from main.forms import UserCreateForm, UserLoginForm
from main.models import User

bp = Blueprint("auth",__name__, url_prefix='/auth')


@bp.route("/signup/", methods = ("GET","POST"))
def signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit():
        user1 = User.query.filter_by(username=form.nickname.data).first()
        user2 = User.query.filter_by(username=form.name.data).first()
        if (not user1) and (not user2):
            user = User(name = form.name.data, username = form.nickname.data, password = generate_password_hash(form.password1.data))
            db.session.add(user)
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.index"))
        else:
            flash("중복된 사용자입니다.")
    return render_template("/auth/signup.html", form = form)

@bp.route("/login/", methods=("POST","GET"))
def login():
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.nickname.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error == None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("main.index"))
        flash(error)
    return render_template("auth/login.html", form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))



def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash("위 기능은 로그인 이후에 가능합니다.")
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
