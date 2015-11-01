import click
import functools

from ctx import exception, version, config, database, document_manager


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
    current_task = doc_mgr.get_active_task()
    if not current_task:
        click.echo('No active tasks')
        return
    click.echo('{}'.format(current_task.id))


@click.command(name='switch')
@click.argument('id')
@inject_document_manager
def cmd_switch(doc_mgr, id):
    task = doc_mgr.get_task_by_id(id)
    current_task = doc_mgr.get_active_task()
    if current_task:
        current_task.set_active(False)
        doc_mgr.update_task(current_task)

    task.set_active(True)
    doc_mgr.update_task(task)

    click.echo('Switched to task {!r}'.format(id))


@click.command(name='new')
@click.option('-d', '--description', default='', help='summary of the task')
@click.argument('id')
@click.pass_context
@inject_document_manager
def cmd_new(doc_mgr, cli_context, id, description):
    try:
        task = doc_mgr.create_task(_id=id)
        if description:
            task.description = description
        doc_mgr.update_task(task)
        click.echo('Created task {!r}'.format(id))
    except exception.DuplicateTaskID:
        click.echo('Cannot create task {!r}: Duplicate task ID'.format(id))
    else:
        cli_context.invoke(cmd_switch, id=id)


@click.command(name='list')
@inject_document_manager
def cmd_list(doc_mgr):
    tasks = doc_mgr.get_tasks()
    for task in tasks.rows:
        click.echo('{} {} {} {}'.format(
            '*' if task.is_active else ' ',
            task.id, task.get('description'), task.total_time))


main.add_command(cmd_info)
main.add_command(cmd_new)
main.add_command(cmd_list)
main.add_command(cmd_version)
main.add_command(cmd_switch)
