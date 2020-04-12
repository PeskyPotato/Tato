from flask_login import UserMixin
from sqlalchemy import func
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))


class Link(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String, nullable=False)
    new_link = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Stats(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(), default=func.now())

    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
