from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.exc import NoResultFound

# initialise the database as an SQLAlchemy object
db = SQLAlchemy()
DB_NAME = "database.db"

from .models import User, Seat


def get_col_count():
    """
    opens the seat layout file and extracts and returns the number of columns.
    """
    with open('chartIn.txt', 'r') as seats_file:
        seats_document = seats_file.readlines()
        seats = [line.split() for line in seats_document]
    return len(seats[0])


# store number of columns in seat layout in variable n_cols
n_cols = get_col_count()


def create_admin():
    """
    function checks for specified email and sets the attribute User.is_admin to true.
    """
    print("create_admin")
    adminmail = 'lion@wolf.com'
    try:
        # filter users by email and if the email is equal to adminmail, set is_admin attribute to true
        admin = db.session.execute(db.select(User).filter_by(email=adminmail)).scalar_one()
        if admin:  # if there is a user with the specified email
            admin.is_admin = True
            db.session.commit()
    except NoResultFound:
        print("no admin found.")
        pass


def create_seats():
    """
    function check database for existing seats. If there are seats found,
    the function passes. Else, the seat layout is read from the specified
    file and instances of the Seat class are stored in the database.
    """
    try:
        # select all implemented seats and store them in implemented_seats
        implemented_seats = db.session.execute(db.select(Seat)).all()

        if len(implemented_seats) > 0:
            print("passing the create_seats function")
            pass
        else:
            raise NoResultFound  # raise error to create seats
    except NoResultFound:  # error when no seats in database
        print("creating seats")
        with open('chartIn.txt', 'r') as seats_file:  # open the seat layout file
            seats_document = seats_file.readlines()  # read in line by line and store these in seat_document
            seats = [line.split() for line in seats_document]  # split the lines into separate lists

        n_cols = len(seats[0])  # the length of the first line in our seat layout is equivalent to the number of columns
        n_rows = len(seats) - 1  # the length of seats is equivalent with the number of rows

        seatnames = []
        # create list with all seat names from the row(i) and the letter
        for i in range(1, n_rows + 1):
            for letter in seats[0]:
                seatnames.append(str(i) + letter)

        seatvalues = []
        # create list of values for availability: 0 means seat is taken, None means seat is free
        for row in seats[1:]:
            for seat in row[1:]:
                if seat == 'X':
                    seatvalues.append(0)
                else:
                    seatvalues.append(None)

        # from the list with seat names and the list of availability create new seats
        # with the specified name and availability
        for i in range(len(seatnames)):
            new_seat = Seat(seat_name=seatnames[i], user_id=seatvalues[i])
            db.session.add(new_seat)
        db.session.commit()  # commit changes to database


def create_app():
    """
    This function creates a Flask app and handles its configuration.
    Routes and functions are imported and Blueprints registered.
    A Login-manager is created
    All necessary tables are created and create_admin and create_seats are
    executed.
    """
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

    # create all necessary tables from the models within the app context,
    # create seats from layout and create admin account
    with app.app_context():
        db.create_all()
        create_seats()
        create_admin()

    # functionality to make the number of columns accessible in the app context
    @app.context_processor
    def inject_cols():
        return dict(cols=n_cols)

    return app
