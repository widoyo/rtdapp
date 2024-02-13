from urllib.parse import urljoin, urlparse

from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, current_app, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from .models import User

bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.username==form.username.data)
        except:
            user = None
        error = ""
        if user is None or not user.check_password(form.password.data):
            error = "User atau Password keliru"
            flash(error)
            return redirect(url_for('auth.login'))
        login_user(user)
        if user.role == 2:
            next = '/admin/pos/' + str(user.pos.id)
        else:
            next = request.args.get('next') or '/admin/'
        if not is_safe_url(next):
            return abort(400)
        return redirect(next)
    else:
        flash(form.errors)
    return render_template('login.html', form=form)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
        
        
@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')