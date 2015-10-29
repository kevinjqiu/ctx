import click
import functools

from ctx import version, config, database, document_manager


def inject_document_manager(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        database.init()
        doc_mgr = document_manager.DocumentManager(database.db)
        return fn(doc_mgr, *args, **kwargs)
    return wrapper


@click.group()
def main():
    pass


@click.command(name='info')
def cmd_info():
    click.echo('version: {}'.format(version.__version__))
    click.echo('db_url: {}'.format(config.DB_URL))


@click.command(name='new')
@click.option('-d', '--description', default='', help='summary of the task')
@click.argument('id')
@inject_document_manager
def cmd_new(doc_mgr, id, description):
    task = doc_mgr.create_task(_id=id)
    click.echo('Created task {!r}'.format(task._id))


@click.command(name='list')
@inject_document_manager
def cmd_list(doc_mgr):
    tasks = doc_mgr.get_tasks()
    import pdb; pdb.set_trace()


main.add_command(cmd_info)
main.add_command(cmd_new)
main.add_command(cmd_list)