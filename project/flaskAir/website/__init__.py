from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.exc import NoResultFound

db = SQLAlchemy()
DB_NAME = "database.db"


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

    # create all necessary tables from the models within the app context
    with app.app_context():
        db.create_all()

    # setup login manager from flask-login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # TODO: implement the 4 standardusers?? pw would be written in plain...

    @app.before_request
    def create_admin():
        adminmail = 'lion@wolf.com'
        try:
            admin = db.session.execute(db.select(User).filter_by(email=adminmail)).scalar_one()
            if admin:
                # set is_admin flag to true if email == lion@wolf.com
                admin.is_admin = True
                db.session.commit()
        except NoResultFound:
            pass

    @app.before_request
    def create_testseat():  # TODO: delete when seat import works!
        try:
            testseat = db.session.execute(db.select(Seat).filter_by(seat_name='0Z')).scalar_one()
            if testseat:
                testseat.user_id = 1

        except NoResultFound:
            testseat = Seat(seat_name='0Z', user_id=1)
            db.session.add(testseat)
            db.session.commit()

    '''
    @app.before_request
    def create_seats():
        if already seats in db:
            skip
        else:
            with open(chartln.txt, "r") as seatlayout:
                read in every row as a line
                for every row in the seat layout:
                    for every seat in row:
                        if seat == 'X':
                            new_seat = Seat(seat_name=seat, user_id=0)
                            db.session.add(new_seat)
                        else:
                            new_seat = Seat(set_name=seat, user_id=None)
                            db.session.add(new_seat)
            db.session.commit()
       '''

    return app
