from flask.ext import sqlalchemy as flask_sqlalchemy


db = None


CONNECTION_STRING = 'postgresql+psycopg2://{user}:{password}@db/ctx'.format(
    user='ctx', password='ctx')


def init_db(app):
    global db
    app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING
    db = flask_sqlalchemy.SQLAlchemy(app)
