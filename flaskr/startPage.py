from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for 
)
from werkzeug.exceptions import abort  
#from flaskr.auth import login_required

from flaskr.db import get_db, row2json_users, row2json_activities, row2json_registered
import click

bp = Blueprint('startPage', __name__,url_prefix='/home')

@bp.route('/')
def index() : 
    db = get_db() 
    users = db.execute(
        "SELECT * FROM users"
    ).fetchall() 
    json = row2json_users(users)
    return json

@bp.route('/actListTime')
def act_list_time() : 
    db = get_db()
    posts = db.execute(
        "SELECT * from activities ORDER BY date_created DESC LIMIT 5"
    ).fetchall()
    json = row2json_activities(posts)
    return json 


@bp.route('/actListCategories/<category>/')
def act_list_categories(category) : 
    db = get_db()    
    posts = db.execute(  
        "SELECT * from activities WHERE category = ? ORDER BY date_created DESC LIMIT 5",(str(category),)
    ).fetchall()

    json = row2json_activities(posts)
    return json
    