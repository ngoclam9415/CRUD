from flask import flash, redirect, render_template, Blueprint
from project.users.oauth import OAuthSignIn
from .forms import RegisterForm
from project import db
from project.models import User
users_blueprint = Blueprint('users', __name__,
                            template_folder='templates'
                            )


@users_blueprint.route('/ register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_exist_fb = User.query.filter_by(email=form.email.data).first()
        if user_exist_fb is None:
            user = User(email=form.email.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('You sign up successful.')
        else:
            flash('Your email have already signed up.')
    return render_template('register.html', form=form)


@users_blueprint.route('/ authorize/<provider >')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@users_blueprint.route('/ callback/<provider >')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    id_social, email = oauth.callback()
    user_exist = User.query.filter_by(email=email).first()
    if (user_exist is None) and (email is not None):
        user = User(
            email=email,
            email_fb=email if provider == “facebook” else None,
            email_tw=email if provider == “twitter” else None,
            id_fb=id_social if provider == “facebook” else None,
            id_tw=id_social if provider == “twitter” else None)
        db.session.add(user)
        db.session.commit()
        flash('You sign up ' + provider + ' successful. ')
    else:
        flash('You have already signed up ' + provider + '.')
    return redirect('/ register')
