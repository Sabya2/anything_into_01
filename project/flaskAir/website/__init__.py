from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.exc import NoResultFound


db = SQLAlchemy()
DB_NAME = "database.db"

from .models import User, Seat

def create_admin():
    print("create_admin")
    adminmail = 'lion@wolf.com'
    try:
        admin = db.session.execute(db.select(User).filter_by(email=adminmail)).scalar_one()
        if admin:
            # set is_admin flag to true if email == lion@wolf.com
            admin.is_admin = True
            # print("admin set")
            db.session.commit()
    except NoResultFound:
        print("no admin found.")
        pass


def create_seats():
    try:
        implemented_seats = db.session.execute(db.select(Seat)).scalars()
        if implemented_seats:
            # print("passing the create_seats function")
            pass

    except NoResultFound:
        print("creating seats")
        with open('chartIn.txt', 'r') as seats_file:
            seats_document = seats_file.readlines()
            seats = [line.split() for line in seats_document]

        n_cols = len(seats[0])
        n_rows = len(seats) - 1

        seatnames = []
        for i in range(1, n_rows + 1):
            for letter in seats[0]:
                seatnames.append(str(i) + letter)

        seatvalues = []
        for row in seats[1:]:
            for seat in row[1:]:
                if seat == 'X':
                    seatvalues.append(0)
                else:
                    seatvalues.append(None)

        for i in range(len(seatnames)):
            new_seat = Seat(seat_name=seatnames[i], user_id=seatvalues[i])
            db.session.add(new_seat)
        db.session.commit()


def create_app():
    app = Flask(__name__)
    # set secret key
    app.config['SECRET_KEY'] = 'secretlol'
    # set path for sqlite3 database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # disable track mod record and suppress warnings about possible overhead
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # initialise
    db.init_app(app)

    # import routes/functions from auth and views
    from .views import views
    from .auth import auth

    # register Blueprints created in auth and views
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import models for database
    from .models import User, Seat

    # setup login manager from flask-login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # TODO: implement the 4 standardusers?? pw would be written in plain...

    # create all necessary tables from the models within the app context, create seats from layout and create admin account
    with app.app_context():
        db.create_all()
        create_seats()
        create_admin()

    ''' This function is not needed when readinSeats() is executed! TODO: delete/comment out

        def create_testseat():  # TODO: delete when seat import works!
            """This function is called in app.context to create a testseat mapped to the admin account"""
            try:
                testseat = db.session.execute(db.select(Seat).filter_by(seat_name='0Z')).scalar_one()
                if testseat:
                    testseat.user_id = 1

            except NoResultFound:
                testseat = Seat(seat_name='0Z', user_id=1)
                db.session.add(testseat)
                db.session.commit()
    '''



    return app

