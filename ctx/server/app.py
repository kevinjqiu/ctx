import flask
from ctx.server import db, document_manager


def get_tasks():
    return flask.jsonify(flask.current_app.document_manager.get_tasks())


def create_app():
    app = flask.Flask('ctx')
    app.config.from_envvar('CTX_SETTINGS')
    db.init_db(app)

    app.document_manager = document_manager.DocumentManager(db.db)

    app.add_url_rule('/task', 'get_tasks', get_tasks, methods=['GET'])
    return app
