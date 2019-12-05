from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for , jsonify
)
from werkzeug.exceptions import abort  
#from flaskr.auth import login_required
from datetime import datetime

from flaskr.db import get_db, row2json_users, row2json_activities, row2json_registered, rowList2json_activities
import click

def current_date() : 
    ans = ""
    count = 0 
    for i in (str(datetime.now())) : 
        if count < 12 : 
            if i not in ['-'," ",":"] : 
                ans += i 
                count += 1
        else : 
            break
    return int(ans)

def strip_tuple(lis) : 
    answer = "" 
    for i in lis : 
        answer = answer + str(i) + ", "
    print(answer)
    return answer.strip(",")

bp = Blueprint('startPage', __name__,url_prefix='/home')

@bp.route('/')
def index() : 
    db = get_db() 
    users = db.execute(
        "SELECT * FROM users"
    ).fetchall() 
    json = row2json_users(users)
    return json

@bp.route('/actListTimeCreated')
def act_list_time_created() : 
    db = get_db()
    posts = db.execute(
        "SELECT * from activities ORDER BY date_created DESC LIMIT 5"
    ).fetchall()
    json = row2json_activities(posts)
    return json 

@bp.route('/actListTimeActivity')
def act_list_time_activity() : 
    db = get_db()
    posts = db.execute(
        "SELECT * from activities ORDER BY date_activity ASC LIMIT 5"
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
    
@bp.route("/actDescList/past/<username>")
def NLP_past(username) : 
    now = current_date() 
    final = []
    activity_ids = []
    db = get_db()
    posts = db.execute(
        "SELECT * FROM registered WHERE username = ?" ,(username,)
    ).fetchall()

    for row in posts : 
        activity_ids.append(row[1])

    for id in activity_ids : 
        answer = db.execute(
            "SELECT * FROM activities WHERE date_activity < ? AND unq_id = ? LIMIT 25",(now,id,)
        ).fetchall()

        final.append(answer)
    json = rowList2json_activities(final)
    return json

@bp.route("/registerForEvent/<username>/<int:id>")
def registerForEvent(username, id) : 
    db = get_db() 
    db.execute(
        "INSERT INTO registered (username, unq_id) VALUES (?,?)",(username,id,)
    )
    db.commit() 
    return jsonify({"status" : 1})#"it works"#jsonify({"staus" : 1})



@bp.route("/actDescList/future/<username>")
def NLP_future(username) : 
    now = current_date() 
    final = []
    activity_ids = []
    db = get_db()
    posts = db.execute(
        "SELECT * FROM registered WHERE username = ?" ,(username,)
    ).fetchall()

    for row in posts : 
        activity_ids.append(row[1])

    for id in activity_ids : 
        answer = db.execute(
            "SELECT * FROM activities WHERE date_activity > ? AND unq_id = ? LIMIT 100",(now,id,)
        ).fetchall()

        final.append(answer)
    json = rowList2json_activities(final)
    return json