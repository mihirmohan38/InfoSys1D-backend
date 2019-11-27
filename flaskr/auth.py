import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Blueprints are ways to organise related views. Views are view functions, code that respond to requests to your application

bp = Blueprint('auth', __name__, url_prefix='/auth') # Creates Blueprint(flask.Blueprint) object with __name__ citing where it is defined.
                                                    # url_prefix will be appended to all urls assocaited with this particular blueprint.

@bp.route('/register', methods=('GET', 'POST')) # '/auth/register' is associated with register() view function, which is called.
def register():
    if request.method == 'POST':
        jsonified_req = request.get_json()
        username = jsonified_req['username']
        password = jsonified_req['password']
        db = get_db() # Our db connection
        error = None

        if not username:                        # Validate username not empty
            error = 'Username is required.'
        elif not password:                      # Validate password not empty
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,) # Alike string formatting, ? is replaced with username
        ).fetchone() is not None:                                  # fetchone() returns one row from the query
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute( # Database connection executes SQLite command, injecting inputusername and password into user table in schema.sql
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()                                 # To commit and save the changes
            return redirect(url_for('auth.login'))      # Redirects to login page

        flash(error)    # Flashes error, if error exists

    return render_template('auth/register.html')    # Rendering of html template for the user, CHANGE TO ROUTE TO ANDROID APP

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        jsonified_req = request.get_json()
        username = jsonified_req['username']
        password = jsonified_req['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()                 # Clear current session, now that validation has completed
            session['user_id'] = user['id'] # Store user id in new session
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html') # Change to route to android app

@bp.before_app_request # Registers below function that runs before view is called
def load_logged_in_user():
    user_id = session.get('user_id')
    session.permanent = True # User remains logged in 
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()     # Removes all stored user information from session dictionary
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view