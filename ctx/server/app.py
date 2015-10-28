import flask
from ctx.server import db


def create_app():
    app = flask.Flask('ctx')
    app.config.from_envvar('CTX_SETTINGS')
    db.init_db(app)
    return app
