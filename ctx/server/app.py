import flask


def create_app():
    app = flask.Flask('ctx')
    return app
