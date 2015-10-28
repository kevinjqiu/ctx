import logging


log = logging.getLogger(__name__)


db = None
server = None


def init():
    log.info('Initialize database')

    from ctx import config
    from couchdb import Server
    global db, server

    server = Server(url=config.DB_URL)
    log.info('db server: {!r}'.format(config.DB_URL))

    try:
        db = server[config.DB_NAME]
    except KeyError:
        db = server.create(config.DB_NAME)
        log.info('db {!r} created'.format(config.DB_NAME))
