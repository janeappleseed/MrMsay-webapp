#!/usr/bin/env python3

import logging
import os

import flask

from mrmsay.__version__ import __version__
from mrmsay import config, logger, say

HERE = os.path.dirname(os.path.realpath(__file__))
COWSAY_PATH = os.path.join(HERE, 'vendor/cowsay/cowsay')

app = flask.Flask(
    'mrmsay',
    template_folder=os.path.join(HERE, 'templates'),
)

@app.route('/')
def index():
    from mrmsay import db, remote
    remote.fetch_comments()
    comment = db.pick_random_comment(300)
    return flask.render_template(
        'index.html',
        version=__version__,
        wisdom_body=say.say(comment.body, cowsay=COWSAY_PATH),
        wisdom_shortlink=comment.short_url,
    )

@app.route('/_say')
def _say():
    from mrmsay import db, remote
    remote.fetch_comments()
    comment = db.pick_random_comment(300)
    return flask.jsonify({
        'wisdom_body': say.say(comment.body, cowsay=COWSAY_PATH),
        'wisdom_shortlink': comment.short_url,
    })

@app.route('/<_>')
def catch_all(_):
    # Heroku talks to flask over HTTP, so we need to manually preserve
    # HTTPS when running on Heroku.
    if '.herokuapp.com' in flask.request.url_root:
        scheme = 'https'
    else:
        scheme = flask.request.environ['wsgi.url_scheme']
    return flask.redirect(
        flask.url_for('index', _scheme=scheme, _external=True),
        code=302,
    )

def main():
    logger.logger_init(level=logging.DEBUG)

    if os.getenv('GH_CREDENTIALS'):
        try:
            user, token = os.getenv('GH_CREDENTIALS').split(':')
        except ValueError:
            sys.stderr.write('[ERROR] Invalid credentials.\n')
            sys.exit(1)
        config.set_credentials(user, token)

    from mrmsay import remote
    remote.fetch_comments()

    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    main()
