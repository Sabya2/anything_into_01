from . import db  # import of our SQLAlchemy object
from flask_login import UserMixin  # TODO: whats UserMixin in flask-login?
from sqlalchemy import func  # import namespace for SQL functions such as now() which gives current time


class Note(db.Model):  # probably not needed, TODO: delete with the func import statement!
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    '''this is how the note is related to ONE user instance and its primary key id'''
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # id is set automatically when the User instance is built
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    notes = db.relationship('Note')

  
'''
class Seat(db.Model):
    """
    currently not working, only as a template to TODO:implement a class for seats
    """
    id = db.Column(db.Integer, primary_key=True)
    seatID = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # relation of seat instance to user
'''
