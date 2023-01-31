from . import db  # import of our SQLAlchemy object
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """
    Define class for users that can log in and book seats
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(False))


class Seat(db.Model):
    """
    Define class for Seats to be booked.
    user_id will store which user has booked this seat:
        None = seat is empty and bookable
        0 = seat is booked by an unknown user as specified in the seatlayout file
        int = The user with this id has booked this seat
    """
    id = db.Column(db.Integer, primary_key=True)
    seat_name = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.Integer, default=None)  # set to 0 if booked by unknown, else to user.id ? 

