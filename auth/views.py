from flask import render_template, request, flash, redirect,url_for
from . import auth
from flask_login import current_user, login_user ,logout_user
from .forms import loginForm
from ..models import User

@auth.route('/login', methods=['GET','POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("Invalid user")
            return redirect(url_for('auth.login'))
        if user.verify_password(form.password.data):
            login_user(user,remember=form.remember_me.data)
            flash('success')
    return render_template('auth/login.html', form=form)
