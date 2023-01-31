from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from .models import User, Seat
from . import db


'''defines routes for "home", "help" and functionality for the website itself'''

# create Blueprint for views
views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    """
    route for homepage: the booked seats for the current user will be displayed as well
    """
    # get seat name for every seat that is in the database if the seat is booked by the current user
    booked_seats = [seat.seat_name for seat in Seat.query.all() if seat.user_id == current_user.id]
    # join the booked seats as a string in the format 1A, 1B, ...
    booked_seats = ', '.join(booked_seats)
    return render_template("home.html", user=current_user, booked_seats=booked_seats)


@views.route('/reservation', methods=['GET', 'POST'])
@login_required
def reservation():
    """
    route for reservation panel:
    post request changes the selected seat user_id attribute to the current user
    flash message about recently booked seats, all booked seats are displayed on the homepage
    """
    if request.method == 'GET':
        all_seats = Seat.query.all()
        return render_template("reservation.html", user=current_user, all_seats=all_seats)
    if request.method == 'POST':
        # empty list to gather names of booked seats
        currently_booking = []
        for seat_id in request.form.getlist('selected_seats'):
            seat = Seat.query.filter_by(id=seat_id).first()
            # set seat attribute user_id to current users id
            seat.user_id = current_user.id
            # append name to list for flash message
            currently_booking.append(seat.seat_name)
            # commit changes to the database
            db.session.commit()
        all_seats = Seat.query.all()
        # join list of recently booked seats to a string
        just_booked = ', '.join(currently_booking)
        flash(f"You have booked the seats {just_booked}.", category="success")
        return render_template("reservation.html", user=current_user, all_seats=all_seats)


@views.route('/export2file', methods=['POST'])
def export2file():
    """
    route to export admin statistics about seats into txt file
    """
    # check admin status
    if current_user.is_admin:
        all_users = User.query.all()
        all_seats = Seat.query.all()
        free_seats = Seat.query.filter_by(user_id=None).all()
        number_all_seats = len(all_seats)
        number_free_seats = len(free_seats)

        list_available_seats = []
        list_taken_seats = []
        for seat in all_seats:
            # if the seat is free
            if seat.user_id == None:
                list_available_seats.append(seat.seat_name)
            # if the seat is taken
            else:
                list_taken_seats.append(seat.seat_name)

        # write everything into the txt file
        with open('./seatinfo.txt', 'a+') as seatinfo:
            timeinfo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if number_all_seats != 0:
                seatinfo.write(f"{timeinfo}:\t seats available: {number_free_seats}\t seats: {number_all_seats}\t{round((number_free_seats / number_all_seats) * 100, 2)} % available\n"
                               f"all available seats: {list_available_seats}\n"
                               f"all taken seats: {list_taken_seats}\n\n")
            else:
                seatinfo.write(f"{timeinfo}:\t seats available: {number_free_seats}\t all seats: {number_all_seats}\n")
            flash('sucessfully written seatinfo', category='success')

        # render updated admin panel
        return render_template("admin.html", user=current_user, all_seats=all_seats, free_seats=free_seats, all_users=all_users)

    else:
        # error msg for non admin users and redirect to their homepage
        flash("This functionality is for admins only!", category='error')
        return redirect(url_for('views.home'))


@views.route("/cancel_seat", methods=["POST"])
def cancel_seat():
    """
    route function to cancel single seats by id
    """
    seat2cancel = Seat.query.filter_by(id=request.form['cancel_seat']).first()
    # set seat user_id to free
    seat2cancel.user_id = None
    db.session.commit()

    # update relevant info to display on the admin panel
    all_users = User.query.all()
    all_seats = Seat.query.all()
    free_seats = Seat.query.filter_by(user_id=None).all()
    return render_template("admin.html", user=current_user, all_seats=all_seats, free_seats=free_seats, all_users=all_users)


@views.route("/cancel_all_seats", methods=["POST"])
def cancel_all_seats():
    """
    route function to cancel all seats of a user
    """
    user_id = request.form['cancel_all_seats']
    seats2cancel = Seat.query.filter_by(user_id=user_id).all()
    # for every seat booked by the user set user_id to free
    for seat in seats2cancel:
        seat.user_id = None
    db.session.commit()  # commit changes to database

    # update relevant info to display on the admin panel
    all_users = User.query.all()
    all_seats = Seat.query.all()
    free_seats = Seat.query.filter_by(user_id=None).all()
    return render_template("admin.html", user=current_user, all_seats=all_seats, free_seats=free_seats, all_users=all_users)


@views.route('/help')
def help():
    """
    route for help page
    """
    return render_template("help.html", user=current_user)
