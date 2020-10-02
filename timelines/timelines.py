import flask
from flask import Flask,url_for,jsonify,g,request
import sqlite3

app=flask.Flask(__name__)
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


@app.route('/getUserTimeline',methods=['GET'])
def getUserTimeline():
    query_parameters=request.args
    username=query_parameters.get('username')
    app.logger.info(username)

    db=get_db()
    getUserTimeline=query_db('SELECT * FROM Tweets WHERE username=?',[username])

    return jsonify(getUserTimeline)


@app.route('/postTweet', methods=['POST'])
def postTweet():
    query_parameters=request.form
    username = query_parameters.get('username')
    text = query_parameters.get('text')

    db= get_db()
    db.execute('INSERT INTO Tweets (username, text) VALUES(?,?)',(username, text))
    res = db.commit()
    getTweets = query_db('SELECT * FROM Tweets')
    return jsonify(getTweets)
