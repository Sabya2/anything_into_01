from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Seat
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


'''defines routes for "login", "signup", "logout" and functionality for AUTHENTICATION'''

# create Blueprint for auth
auth = Blueprint('auth', __name__)


@auth.route('/admin', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def admin():
    if request.method == 'GET':
        if current_user.is_admin:
            return render_template('admin.html',
                                   user=current_user,
                                   all_users=User.query.all(),
                                   all_seats=Seat.query.all(),
                                   free_seats=Seat.query.filter_by(user_id=None).all())
            # renders admin page and passes all users and all seat objects
        else:
            flash("This area is for admins only.", category='error')
            return redirect(url_for('views.home'))
    if request.method == 'POST':
        # functionality here?
        flash("admin accessed with POST")
        return redirect(url_for('auth.admin'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        login_password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:  # checks if the user exists
            if check_password_hash(user.password, login_password):  # checks users password
                flash('Logged in successfully!', category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('This user does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # asking for the input information
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        user = User.query.filter_by(email=email).first()  # retrieve users with this email
        if user:  # if email already registered
            flash('This email is already registered.', category='error')
        elif len(email) < 4: # checking the length of the email
            flash('email must be longer than 3 characters.', category='error')
        elif len(firstname) < 2: # checking the length of the firstname
            flash('First name must be longer than 1 character.', category='error')
        elif len(lastname) < 2:  # checking the length of the lastname
            flash('Last name must be longer than 1 character.', category='error')
        elif len(password) < 7:  # checking the length of the password
            flash('Passwords must be at least 7 characters.', category='error')
        elif password != confirm_password:  # checking the if the passwords match
            flash('Passwords do not match.', category='error')
        else:   # creates the new user and stores it in the database 
            new_user = User(email=email,
                            firstname=firstname,
                            lastname=lastname,
                            password=generate_password_hash(password, method='sha256'),
                            is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully.', category='success')
            return redirect(url_for('views.home')) # redirects the user to the homepage after creating the account

    return render_template("signup.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():  # to logout, using flask_login library
    flash('Logged out! Have a nice day :3', category='success')
    logout_user()
    return redirect(url_for('auth.login'))
