import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        for result in db.cursor().execute(f.read().decode('utf8'), multi=True): # if multi True, return iterator
            if result.with_rows:
                print("Rows produced by statement '{}':".format(result.statement))
                print(result.fetchall())
            else:
                print("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))

@click.command('init-db') # flask command
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app): # factory need to call this
    app.teardown_appcontext(close_db) # cleanup after response
    app.cli.add_command(init_db_command) # add into flask commands if u wanna call this, 'flask init-db'

def get_db(dns=None):

    # このdnsはcurrent_app.config['DATABASE']で定義？
    if dns is None:
        dns = {
            'user': 'mysql',
            'host': 'localhost',
            'password': 'NewPassword',
            'database': 'kaggle'
        }

    if 'db' not in g:
        g.db = mysql.connector.connect(**dns)

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
