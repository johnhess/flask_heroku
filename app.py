import datetime
import os

from flask import Flask
from flask import render_template
from flask import request
import redis


app = Flask(__name__)

REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost')


def get_db():
    return redis.StrictRedis.from_url(REDIS_URL)

def store_message(message):
    get_db().set(datetime.datetime.utcnow(), message.encode('utf-8'))

def get_messages():
    """All messages in reverse chronological order."""
    db = get_db()
    return [
        db.get(key).decode('utf-8') 
        for key in reversed(sorted(db.keys()))
    ]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uhoh-dj')
def uhoh():
    return render_template('uhoh-dj.html')

@app.route('/reflected')
def reflected_xss():
    who = request.args.get('name', 'friend')
    return 'Hello, {}.'.format(who)

@app.route('/stored', methods=['GET', 'POST'])
def stored_xss():
    # store the new message, if there is one
    if request.method == 'POST':
        store_message(request.form.get('message'))
    # either way, give back the list of messages
    return render_template(
        'guestbook.html',
        messages=get_messages()
    )

@app.route('/nuke')
def nuke():
    get_db().flushall()
    return 'flushed.'


if __name__ == '__main__':
    app.run()