import click
import functools

from ctx import (
    action, version, config, database, document_manager)


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


@click.command(name='version')
def cmd_version():
    click.echo('version: {}'.format(version.__version__))
    click.echo('db_url: {}'.format(config.DB_URL))


@click.command(name='info')
@inject_document_manager
def cmd_info(doc_mgr):
    current_task = doc_mgr.get_current_task()
    if not current_task:
        click.echo('No active tasks')
        return
    click.echo('{}'.format(current_task.id))


@click.command(name='new')
@click.option('-d', '--description', default='', help='summary of the task')
@click.argument('id')
@inject_document_manager
def cmd_new(doc_mgr, id, description):
    try:
        task = doc_mgr.create_task(_id=id)
        current_task = doc_mgr.get_current_task()
        if current_task:
            current_task.set_active(False)
        task.set_active(True)
        doc_mgr.update_task(task)
    except exception.DuplicateTaskID:
        click.echo('Cannot create task {!r}: Duplicate task ID'.format(id))
    else:
        click.echo('Created task {!r}'.format(task._id))
        return task


@click.command(name='list')
@inject_document_manager
def cmd_list(doc_mgr):
    tasks = doc_mgr.get_tasks()
    for task in tasks.rows:
        click.echo('{} {} {}'.format(task.id, task.get('description'), task.total_time))


main.add_command(cmd_info)
main.add_command(cmd_new)
main.add_command(cmd_list)
main.add_command(cmd_version)
