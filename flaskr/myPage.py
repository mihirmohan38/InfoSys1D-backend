from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for 
)
from werkzeug.exceptions import abort  
#from flaskr.auth import login_required

from flaskr.db import get_db, row2json_users, row2json_activities, row2json_registered
import click

bp = Blueprint('myPage', __name__,url_prefix='/myPage')

@bp.route("/")
def index() : 
    return "please log in to view the page"

@bp.route('/<user>')
def myact(user) : 
    db = get_db() 
    activities = db.execute(
        "SELECT * FROM registered WHERE username = ?",(str(user),)
    ).fetchall() 
    json = row2json_registered(activities)
    return json

@bp.route("/<int:act_id>")
def getAct(act_id) : 
    db = get_db() 
    activity = db.execute(
        "SELECT * FROM activities WHERE unq_id = ?", (act_id)
    ).fetchone() 

    json = row2json_activities(activity)
    return json