from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for , jsonify
)
from werkzeug.exceptions import abort  
#from flaskr.auth import login_required
from datetime import datetime

from flaskr.db import get_db, row2json_users, row2json_activities, row2json_registered, rowList2json_activities , rowList2json
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

bp = Blueprint('notification', __name__,url_prefix='/notification')

@bp.route('/')
def index() : 
    return jsonify({"message" : "select user"})


@bp.route('/<username>')
def getNotification(username) : 
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
            "SELECT * FROM activities WHERE date_activity > ? AND date_activity < ? AND unq_id = ?",(now,now + 20000,id,)
        ).fetchall()

        final.append(answer)
    json = rowList2json(final)
    return json