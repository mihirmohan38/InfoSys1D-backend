from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db, row2json_activities, row2json_users, row2json_registered


bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT unq_id, title, category,date_created, date_activity,creator,venue,ppl,image_uri,descrip,max_ppl'
        ' FROM activities p JOIN users u ON p.creator = u.username'
        ' ORDER BY date_created DESC'
    ).fetchall()
    return jsonify({"hello": "hi"})

@bp.route('/create', methods=('GET', 'POST'))
#@login_required
def create():
    jsonified_req = request.get_json()
    title = jsonified_req['title']
    date_activity = jsonified_req['date_activity']
    people = jsonified_req['ppl']
    max_people = jsonified_req['max_ppl']
    imageURI = jsonified_req['image_uri']
    location = jsonified_req['venue']
    category = jsonified_req['category']
    details = jsonified_req['description']
    telegram_group = jsonified_req["telegram_group"]
    username = jsonified_req["creator"]


    db = get_db()
    db.execute(
        'INSERT INTO activities (title, date_created, date_activity, ppl, max_ppl, image_uri, venue, category, descrip, creator,telegram_group) VALUES (?, DATE(), ?, ?, ?, ?, ?, ?, ?, ?,?)',
        (title, date_activity, people, max_people, imageURI, location, category, details, username,telegram_group)
        #("3","3","3","3","3","3","3","3","3","3" )
    )
    db.commit()
    return jsonify({})



def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT unq_id, title,date_created,date_activity,ppl,max_ppl,image_uri,venue,category, descrip, creator'
        ' FROM post p JOIN user u ON p.creator = u.username'
        ' WHERE p.unq_id = ?',
        (id)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id,))

    if check_author and post['creator'] != g.user['id']:
        abort(403)

    return row2json_activities(post) 

    

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
#@login_required
def update(id):
    post = get_post(id)
    jsonified_req = request.get_json()
    title = jsonified_req['title']
    date_activity = jsonified_req['date_activity']
    people = jsonified_req['people']
    max_people = jsonified_req['max_people']
    imageURI = jsonified_req['imageURI']
    location = jsonified_req['location']
    category = jsonified_req['category']
    details = jsonified_req['details']

    db = get_db()
    db.execute(
        'UPDATE post SET title = ?,date_activity=?,ppl=?,max_ppl=?,image_uri=?,venue = ?, category = ?, descrip = ?'
        ' WHERE unq_id = ?',
        (title,date_activity,people,max_people,imageURI, location, category, details, id)
    )
    db.commit()
    return jsonify({})

@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE unq_id = ?', (id,))
    db.commit()
    return jsonify({})