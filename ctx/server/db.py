from couchdb import Server

server = None
db = None


def init_db(app):
    app.logger.info('Initializing db')
    global server, db

    db_url, db_name = app.config['DB_URL'], app.config['DB_NAME']
    app.logger.info('DB_URL={}'.format(db_url))

    server = Server(url=db_url)

    try:
        db = server.create(db_name)
    except:
        db = server[db_name]

    app.db = db
