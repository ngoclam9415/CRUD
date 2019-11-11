from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager, db
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request, url_for


class Permission:
    ADMIN = 1


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.Unicode(128))
    password_hash = db.Column(db.String(128))
    social_id = db.Column(db.BIGINT)
    social_type = db.Column(db.Unicode(64))
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            'email': self.username,
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
