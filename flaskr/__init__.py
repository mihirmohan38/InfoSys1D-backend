import os 
from flask import Flask 
from flaskr.db import get_db
import click
import json

def create_app(test_config = None) : 
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev", 
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite')

    )

    if test_config is None : 
        app.config.from_pyfile("config.py", silent = True )
    else : 
        app.config.from_mapping(test_config)
    
    try :
        os.mkdir(app.instance_path)
    except OSError : 
        pass



    @app.route("/hello")
    def hello(): 
        inst = get_db().execute(
            "SELECT password FROM users WHERE username = 'mihir'"
            #"SELECT * FROM users"
            
        ).fetchall()
        click.echo(inst)
        return "hello"

    from . import db, startPage, myPage
    
    db.connectApp2db(app)
    app.register_blueprint(startPage.bp)
    app.register_blueprint(myPage.bp)
    #app.register_blueprint(home.bp)
    #app.add_url_rule("/", endpoint="index")
    return app 