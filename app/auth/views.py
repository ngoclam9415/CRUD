from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from ..models import User
from ..utils.input_validator import valid_email, valid_password, validate_input
from . import auth
from .auth_providers import OAuthSignIn


@auth.route('/login', methods=['GET', 'POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':
        user = User.query.filter_by(email=email.lower()).first()

        if user is not None and user.verify_password(password):
            login_user(user, True)
            return redirect(url_for('auth.login'))

        flash('Invalid email or password.')
    return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':
        input_error = ""

        is_valid_input, input_error = validate_input(
            {"email": email, "password": password})

        if not is_valid_input:
            flash(input_error, 'error')
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(email=email.lower()).first()

        if user is not None:
            registered_platform = "" if not user.social_type else user.social_type

            flash(u'Email already taken with ' + registered_platform, 'error')
            return redirect(url_for('auth.register'))

        user = User(email=email, password=password,
                    social_type='EMAIL', name="Unknown", social_id=0)
        db.session.add(user)
        db.session.commit()

        flash(u'Your registration was successful!', 'success')
    return render_template('auth/register.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/authorize/<provider>', methods=['GET', 'POST'])
def oauth_authorize(provider):
    print(request.form)
    if not current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('auth.login'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, name, email, social_platform = oauth.callback()

    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(social_id=social_id, name=name, email=email,
                    social_type=social_platform)
        db.session.add(user)
        db.session.commit()

    if int(user.social_id) != int(social_id):
        flash("Email Address is Already Registered With : " + user.social_type)
        return redirect(url_for('auth.login'))

    login_user(user, True)

    return redirect(url_for('auth.login'))
