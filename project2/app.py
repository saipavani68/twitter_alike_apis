#!/usr/bin/env python3

# See <https://code-maven.com/using-templates-in-flask>

from flask import Flask, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import logging

app = Flask('app')
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
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        

#User registration

@app.route('/register', methods=['POST'])
def createUser():
    query_parameters = request.form

    username = query_parameters.get('username')
    email = query_parameters.get('email')
    password = query_parameters.get('password')
    hashed_password = generate_password_hash(password, "sha256") #Generating hash for the user entered password
    
    app.logger.info(username)
    
    db= get_db()
    count = query_db('SELECT COUNT(*) as count FROM users WHERE username = ?', [username])
    if(count[0].get('count') > 0):                             #returns 400 error if username already exists
        return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Username already taken"})
    elif username== None or username=='' or password== None or password=='' or email==None or email=='':         #returns 400 error if either username or password or email are not provided.
        return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter(s)"})
    else:                                                      #new user successful registration
        db.execute('INSERT INTO users (username, email, password) VALUES(?,?,?)',(username, email, hashed_password))
        res = db.commit()
        return jsonify({"statusCode": 200, "message": "You have successfully registered!"})


#Authenticating user

@app.route('/login', methods=['POST'])
def authenticateUser():
    query_parameters = request.form
    
    username = query_parameters.get('username')
    password = query_parameters.get('password')
    
    db= get_db()
    result = query_db('SELECT password FROM users WHERE username = ?', [username])
    
    hashed_password = result[0].get('password')
    validate_user = check_password_hash(hashed_password, password)    #checking if user entered password is equal to the hashed password in db
    if validate_user:
        return jsonify(validate_user)
    else:
        return jsonify({"statusCode": 401, "error": "Unauthorized", "message": "Login failed: Invalid username or password" })



# Allowing user to follow another user

@app.route('/follow', methods=['POST'])
def addFollower():
    query_parameters = request.form
    
    username = query_parameters.get('username')
    usernameToFollow = query_parameters.get('usernameToFollow')
    
    db= get_db()
    db.execute('INSERT INTO user_following (username, usernameToFollow) VALUES(?,?)',(username, usernameToFollow))
    res = db.commit()
    
    #Returns 400 error when username or usernameToFollow are not provided.
    if username == '' or username == None or usernameToFollow == None or usernameToFollow == '':
        return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter(s)" })
    else:
        return jsonify({"statusCode":200, "message": "You are successfully following {}!".format(usernameToFollow)})
    

#Allowing user to unfollow another user

@app.route('/unfollow', methods=['POST'])
def removeFollower():
    query_parameters = request.form
       
    username = query_parameters.get('username')
    usernameToRemove = query_parameters.get('usernameToRemove')
    
    db= get_db()
    db.execute('DELETE FROM user_following WHERE username=? AND usernameToFollow=?',(username, usernameToRemove))
    res = db.commit()
    
    #Returns 400 error when username or usernameToFollow are not provided.
    if username == '' or usernameToRemove == '' or username == None or usernameToRemove == None:
        return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter(s)" })
    else:
        return jsonify({"statusCode":200, "message": "You have successfully unfollowed {}!".format(usernameToRemove)})