#!/usr/bin/env python3

# See <https://code-maven.com/using-templates-in-flask>

from flask import Flask, request, jsonify, g
import sqlite3
import logging

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('users.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/register', methods=['POST'])
def createUser():
    query_parameters = request.form

    username = query_parameters.get('username')
    email = query_parameters.get('email')
    password = query_parameters.get('password')
    
    app.logger.info(username)
    
    db= get_db()

    createNewUser = db.execute('INSERT INTO users (username, email, password) VALUES(?,?,?)',(username, email, password))
    res = db.commit()
    
    getusers = query_db('SELECT * FROM users')
    return jsonify(getusers)