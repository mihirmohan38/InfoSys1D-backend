import sqlite3 
import click 
from flask import current_app, g 
from flask.cli import with_appcontext
import simplejson
#from sqlobject import * 

def get_db() : 
    if "db" not in g : 
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], 
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row 
    
    return g.db


def close_db(e = None ) : 
    db = g.pop('db', None)

    if db is not None : 
        db.close() 

def init_db() : 
    db = get_db()

    with current_app.open_resource("schema.sql") as f : 
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext 
def init_db_command() : 
    init_db() 
    click.echo("Initialized the database")

def connectApp2db(app) : 
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)       


def row2json_users(table) :
    users = []
    user_dict = {} 
    answer = {}
    i = 0 
    for row in table : 
        user_dict = {
            "username" : row[0],
            "password" : row[1]
        }
        users.append(user_dict)
    for user in users : 
        answer[i] = user
        i += 1 

 
    return simplejson.dumps(users)

def row2json_activities(table) : 
    activities = []
    for row in table : 

        act_dict = {
            "unq_id" : row[0], 
            "category" : row[1],
            "date_created" : str(row[2]),
            "date_activity" : str(row[3]), 
            "creator" : row[4]
        }

        activities.append(act_dict)
    return simplejson.dumps(activities)

def row2json_registered(table) : 
    reg = []
    for row in table :
        reg_dict = {
            "username" : row[0],
            "activity" : row[1]
        }
        reg.append(reg_dict)

    json_dict = {}
    for i in reg : 
        username = i["username"]
        activity = i["activity"]
        if username in json_dict : 
            json_dict[username].append(activity)
        else : 
            json_dict[username] = [activity]
        


    return simplejson.dumps(json_dict)