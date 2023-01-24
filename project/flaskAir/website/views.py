from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import json


'''defines routes for "home", "help" and functionality for the website itself'''

# create Blueprint for views
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    TODO: change to include personal info of current_user OR directly go to 'reserve Seats' view!
    """

    return render_template("home.html", user=current_user)



''' 
TODO: Take this as an example how functionality in Flask can be constructed with jsonify

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
'''
@views.route('/help')
def help():
    return render_template("help.html", user=current_user)
