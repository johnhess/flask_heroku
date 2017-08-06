import datetime
import os

import flask
import redis


app = flask.Flask(__name__)

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost')


def get_db():
    return redis.StrictRedis.from_url(REDIS_URL)

def get_messages():
    """All messages in reverse chronological order."""
    db = get_db()
    return [
        db.get(key).decode('utf-8') 
        for key in reversed(sorted(db.keys()))
    ]

@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/reflected')
def reflected_xss():
    return 'Hello, {}.'.format(flask.request.args.get('name', 'friend'))

@app.route('/stored', methods=['GET', 'POST'])
def stored_xss():
    db = get_db()
    
    # store the new message, if there is one
    if flask.request.method == 'POST':
        message = flask.request.form.get('message', '').encode('utf-8')
        db.set(datetime.datetime.utcnow(), message)

    # give back the list of messages
    messages = get_messages()

    return flask.render_template('stored.html', messages=messages)

@app.route('/nuke')
def nuke():
    get_db().flushall()
    return 'flushed.'


if __name__ == '__main__':
    app.run()