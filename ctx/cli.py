import click
import functools

from ctx import (
    action, version, config, database, document_manager, exception)


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
    action.new_task(doc_mgr, id, description)


@click.command(name='list')
@inject_document_manager
def cmd_list(doc_mgr):
    tasks = doc_mgr.get_tasks()
    for task in tasks.rows:
        click.echo("{} {}".format(task.doc.id, task.doc.get('description')))


main.add_command(cmd_info)
main.add_command(cmd_new)
main.add_command(cmd_list)
