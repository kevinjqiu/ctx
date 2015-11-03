import os


ctx_cfg = os.environ.get('CTX_CFG', 'default')


config_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           '..', 'configurations',
                                           '{}.cfg'.format(ctx_cfg)))


if not os.path.exists(config_file):
    raise RuntimeError('Config file {!r} not found'.format(config_file))


exec(open(config_file).read())
