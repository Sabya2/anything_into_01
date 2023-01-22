from . import db  # import of our SQLAlchemy object
from flask_login import UserMixin
from flask_security import RoleMixin


""" Relation between roles and users is stored in this table """
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    """ Define class for users that can login and book seats """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )


class Seat(db.Model):
    """ Define class for Seats to be booked """
    id = db.Column(db.Integer, primary_key=True)
    seatID = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # relation of seat instance to user


class Role(db.Model, RoleMixin):
    """ Define class for roles admin and user """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))
