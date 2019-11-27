from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        jsonified_req = request.get_json()
        title = jsonified_req['title']
        date_created = jsonified_req['date_created']
        date_activity = jsonified_req['date_activity']
        people = jsonified_req['people']
        max_people = jsonified_req['max_people']
        imageURI = jsonified_req['imageURI']
        location = jsonified_req['location']
        category = jsonified_req['category']
        details = jsonified_req['details']
        error = None

        if not title:
            error = 'Title is required.'
        if not location:
            error = 'Location is required'
        if not category:
            error = 'Category is required'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title,date_created,date_activity,people,max_people,imageURI,location,category, details, creator)'
                ' VALUES (?,?,? ?, ?,?,?,?,?,?)',
                (title,date_created,date_activity,people,max_people,imageURI,location,category, details, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, location, category, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        jsonified_req = request.get_json()
        title = jsonified_req['title']
        date_created = jsonified_req['date_created']
        date_activity = jsonified_req['date_activity']
        people = jsonified_req['people']
        max_people = jsonified_req['max_people']
        imageURI = jsonified_req['imageURI']
        location = jsonified_req['location']
        category = jsonified_req['category']
        details = jsonified_req['details']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, date_created=?,date_activity=?,people=?,max_people=?,imageURI=?,location = ?, category = ?, details = ?'
                ' WHERE id = ?',
                (title,date_created,date_activity,people,max_people,imageURI, location, category, details, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))