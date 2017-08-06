import os

import flask

app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/reflected')
def reflected_xss():
    return 'Hello, {}.'.format(flask.request.args.get('name', 'friend'))

@app.route('/stored', methods=['GET', 'POST'])
def stored_xss():
    messages = ['foo', 'bar']
    if flask.request.method == 'POST':
        messages.append('New')

    return flask.render_template('stored.html', messages=messages)


if __name__ == '__main__':
    app.run()