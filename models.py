from . import db
from flask_login import UserMixin
from . import login_manager
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def login_user(user_id):
    return User.query.get(init(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        raise AssertionError('password is not a readable attribute')

    @password.setter
    def password(self, passord):
        self.password_hash = generate_password_hash(passord)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class WebSite(db.Model):
    __tablename__ = 'websites'
    id = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.String(64), unique=True)
    sitestatus = db.Column(db.Boolean, default=True)
    apppool = db.Column(db.String(64))
    Path = db.Column(db.String(128))
    domains = db.relationship('SiteDomain', backref='site', lazy='dynamic')


class SiteDomain(db.Model):
    __tablename__ = 'sitedomain'
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(64))
    status_code = db.Column(db.String(64))
    ignore = db.Column(db.Boolean)
    time = db.Column(db.DateTime , default=datetime.utcnow)
    site_id = db.Column(db.Integer, db.ForeignKey('websites.id'))
