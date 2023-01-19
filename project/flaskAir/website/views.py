from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


'''defines routes for "home", "help" and functionality for the website itself'''

views = Blueprint('views', __name__)  # load in views as flask blueprint


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    This should maybe include only the personal info of current_user?
    Or all seats idk
    """
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/help')  # default methods = GET only
def helppage():
    return render_template('helppage.html', user=current_user)


'''This is old funcionality from the tutorial (techwithtim)'''


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
