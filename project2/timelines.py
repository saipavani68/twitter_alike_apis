import flask
from flask import Flask,url_for,jsonify,g,request
from datetime import datetime
import sqlite3

app=Flask('timelines')
app.config.from_envvar('APP_CONFIG')


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

@app.cli.command('init')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = make_dicts
    return db


#Retrieve the 25 most recent tweets of the user

@app.route('/getUserTimeline',methods=['GET'])
def getUserTimeline():
    query_parameters=request.args
    username=query_parameters.get('username')

    db=get_db()
    
    #Returns 400 error when username is not provided.
    if username == '' or username == None:
        return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter" })
    else:
        getUserTimeline=query_db('SELECT * FROM Tweets WHERE username=? ORDER BY timestamp DESC LIMIT 25',[username])
        return jsonify(getUserTimeline)


#Retrieve the 25 most recent tweets from all users
 
@app.route('/getPublicTimeline',methods=['GET'])
def getPublicTimeline():
    db=get_db()
    getPublicTimeline=query_db('SELECT * FROM Tweets ORDER BY timestamp DESC LIMIT 25')

    return jsonify(getPublicTimeline)

#Returns recent(limited to 25) tweets from all users that this user follows.

@app.route('/getHomeTimeline',methods=['GET'])
def getHomeTimeline():
    db=get_db()
    query_parameters=request.args
    username=query_parameters.get('username')
    
    #Returns 400 error when username is not provided.
    if username == '' or username == None:
        return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter" })
    else:
        getHomeTimeline=query_db('SELECT * from Tweets WHERE username IN (SELECT usernameToFollow FROM user_following WHERE username=?) ORDER BY timestamp DESC LIMIT 25',[username])
        return jsonify(getHomeTimeline)


@app.route('/postTweet', methods=['POST'])
def postTweet():
    query_parameters=request.form
    username = query_parameters.get('username')
    text = query_parameters.get('text')
    timestamp = datetime.utcnow()

    db= get_db()
    result = query_db('SELECT COUNT(*) as count FROM users WHERE username = ?', [username])
    
    #Returns 400 error when username or text is not provided.
    if username == '' or username == None or text == '' or text== None:
        return jsonify({"statusCode": 400, "error": "Bad Request", "message": "Invalid parameter" })
    
    #Only an existing user can post a tweet
    elif result[0].get('count') > 0:
        db.execute('INSERT INTO Tweets (username, text, timestamp) VALUES(?,?, ?)',(username, text, timestamp))
        res = db.commit()
        getTweets = query_db('SELECT * FROM Tweets')
        return jsonify({"statusCode": 200})
    else:
        return jsonify({"message": "Username doesn't exist. If you are a new user please register, or if you are an existing user please sign in"})
