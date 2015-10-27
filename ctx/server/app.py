import flask
from ctx.server import db


def create_app():
    app = flask.Flask('ctx')
    db.init_db(app)
    return app
