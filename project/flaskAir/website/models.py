from . import db  # import of our SQLAlchemy object
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """ Define class for users that can log in and book seats """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(False))
    # backref to user: Seat.user will give the corresponding user
    # seats = db.relationship('Seat', backref='user')


class Seat(db.Model):
    """ Define class for Seats to be booked """
    id = db.Column(db.Integer, primary_key=True)
    seat_name = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.Integer, default=None)  # set to 0 if booked by unknown, else to user.id ? 
    # TODO:try if None value works for db.Integer
